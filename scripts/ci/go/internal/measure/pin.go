package measure

import (
	"bytes"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"

	"github.com/hhh-pa/python-code-snippet/scripts/ci/go/internal/snipcore"
)

// PinRepeatDefault runs two Pin counts per case: native counts
// agree to ~0.1%, enough to catch instrument flakiness without
// paying for more slow runs.
const PinRepeatDefault = 2

// PinUsable reports whether Pin count runs can execute: the pin
// launcher resolves and the inscount tool file exists.
func PinUsable(pinBin, tool string) bool {
	if pinBin == "" || tool == "" {
		return false
	}
	if _, err := os.Stat(tool); err != nil {
		return false
	}
	if strings.Contains(pinBin, string(os.PathSeparator)) {
		info, err := os.Stat(pinBin)
		return err == nil && info.Mode()&0o111 != 0
	}
	_, err := exec.LookPath(pinBin)
	return err == nil
}

// PinVersion probes `pin -version` for report provenance, or nil
// when the launcher cannot answer. Compared runs must share one
// Pin version: counts are only comparable within a version.
func PinVersion(pinBin string) *string {
	stdout, _, err := snipcore.Run([]string{pinBin, "-version"}, nil, 30)
	if err != nil {
		return nil
	}
	for _, line := range strings.Split(string(stdout), "\n") {
		if trimmed := strings.TrimSpace(line); trimmed != "" {
			return &trimmed
		}
	}
	return nil
}

// IsPinTimeout reports whether a PinOnce error text is a deadline
// timeout rather than a crash: timeouts mean the input exceeds
// the instrument's budget, so the case degrades to a skip.
func IsPinTimeout(runErr string) bool {
	return strings.Contains(runErr, "TIMEOUT")
}

// EnsureAllocShim builds the LD_PRELOAD allocation-counting shim on
// demand: it compiles scripts/ci/instrumentation/allocshim.c with cc
// into a fresh temp dir and returns the .so path. It fails when the
// platform has no LD_PRELOAD (non-Linux), no C compiler, or the
// build fails.
func EnsureAllocShim(root string) (string, error) {
	if runtime.GOOS != "linux" {
		return "", errors.New("needs Linux (LD_PRELOAD)")
	}
	cc, err := exec.LookPath("cc")
	if err != nil {
		cc, err = exec.LookPath("gcc")
		if err != nil {
			return "", errors.New("needs a C compiler (cc not found)")
		}
	}
	src := filepath.Join(root, "scripts", "ci", "instrumentation", "allocshim.c")
	if _, err := os.Stat(src); err != nil {
		return "", fmt.Errorf("shim source missing at %s", src)
	}
	buildDir, err := os.MkdirTemp("", "snip-alloc-shim-")
	if err != nil {
		return "", err
	}
	out := filepath.Join(buildDir, "alloc_shim.so")
	stdout, stderr, runErr := snipcore.Run(
		[]string{cc, "-shared", "-fPIC", "-O2", "-o", out, src, "-ldl"}, nil, 120)
	_ = stdout
	if runErr != nil {
		tail := strings.TrimSpace(string(stderr))
		if tail != "" {
			if lines := strings.Split(tail, "\n"); len(lines) > 0 {
				tail = strings.TrimSpace(lines[len(lines)-1])
			}
			return "", fmt.Errorf("build failed: %s", tail)
		}
		return "", fmt.Errorf("build failed: %v", runErr)
	}
	return out, nil
}

// PinOnce runs inner once under Intel Pin with the inscount tool
// and returns stdout, the total instruction count, and the total
// allocated bytes parsed from the run's stderr. When allocShim names
// a built shim .so, it is LD_PRELOADed into the Pin run so the
// same run yields both the instruction count and the cumulative
// allocated bytes; a missing shim total after a successful exit is
// a harness failure ("pin alloc output unreadable"), since silently
// dropping a tracked measure is worse than a red case. With no
// shim, alloc is nil when the marker is absent. The Python harness
// has no JVM leg, so this is the plain native recipe with no JVM
// signal flags.
func PinOnce(pinBin, tool string, inner []string, input []byte, timeout int, allocShim string) (stdout []byte, count int64, alloc *int64, runErr string) {
	outFile, err := tempPinFile()
	if err != nil {
		return nil, 0, nil, "pin output unreadable: " + err.Error()
	}
	defer os.Remove(outFile)
	cmd := []string{pinBin, "-t", tool, "-o", outFile, "--"}
	cmd = append(cmd, inner...)
	var extraEnv []string
	if allocShim != "" {
		prev := os.Getenv("LD_PRELOAD")
		preload := allocShim
		if prev != "" {
			preload = allocShim + ":" + prev
		}
		extraEnv = []string{"LD_PRELOAD=" + preload}
	}
	stdout, stderr, err := snipcore.RunEnv(cmd, input, timeout, extraEnv)
	var timeoutErr *snipcore.TimeoutError
	if errors.As(err, &timeoutErr) {
		return nil, 0, nil, fmt.Sprintf("TIMEOUT (>%ds)", timeout)
	}
	if err != nil {
		var exitErr *exec.ExitError
		if errors.As(err, &exitErr) {
			tail := string(bytes.TrimSpace(stderr))
			return nil, 0, nil, fmt.Sprintf("exit %d: %s", exitErr.ExitCode(), tail)
		}
		return nil, 0, nil, fmt.Sprintf("execution error: %v (%s)", err, string(stderr))
	}
	raw, err := os.ReadFile(outFile)
	if err != nil {
		return nil, 0, nil, "pin output unreadable: " + err.Error()
	}
	count, err = ParsePinCount(string(raw))
	if err != nil {
		return nil, 0, nil, err.Error()
	}
	if n, found := ParseAllocBytes(string(stderr)); found {
		alloc = &n
	} else if allocShim != "" {
		return nil, 0, nil, "pin alloc output unreadable: no snip_alloc_total_bytes line"
	}
	return stdout, count, alloc, ""
}

func tempPinFile() (string, error) {
	tmp, err := os.CreateTemp("", "snip-pin-*.out")
	if err != nil {
		return "", err
	}
	name := tmp.Name()
	tmp.Close()
	return name, nil
}

// MeasureCasePin runs the Pin inscount phase for one case: pinRepeat
// counts of execCmd under Pin. Each run yields both the
// instruction count and (when allocShim names a built shim) the
// allocated bytes, returned as a summary holding just those two
// instrument signals. It returns a skip reason when the case
// exceeded the Pin budget (other data stays valid), or an error
// when the case crashes or mismatches under Pin. The first Pin run
// gates correctness, so pin-only sweeps (--repeat 0) still verify
// output.
func MeasureCasePin(label, caseName string, execCmd []string, inputPath, outputPath string, pinBin, pinTool string, pinRepeat, pinTimeout int, allocShim string) (*CaseSummary, *string, error) {
	expectedBytes, err := os.ReadFile(outputPath)
	if err != nil {
		return nil, nil, fmt.Errorf("read output file: %w", err)
	}
	expected := snipcore.Normalize(expectedBytes)

	inputBytes, err := os.ReadFile(inputPath)
	if err != nil {
		return nil, nil, fmt.Errorf("read input file: %w", err)
	}

	var counts []float64
	var allocs []float64
	for i := 0; i < pinRepeat; i++ {
		stdout, count, alloc, runErr := PinOnce(pinBin, pinTool, execCmd, inputBytes, pinTimeout, allocShim)
		if runErr != "" {
			if IsPinTimeout(runErr) {
				skip := runErr
				fmt.Fprintf(os.Stderr, "warning: %s/%s: pin skipped (%s)\n",
					label, caseName, runErr)
				return nil, &skip, nil
			}
			return nil, nil, fmt.Errorf("pin: %s", runErr)
		}
		if i == 0 && !bytes.Equal(snipcore.Normalize(stdout), expected) {
			got := string(snipcore.Normalize(stdout))
			want := string(expected)
			if len(got) > 100 {
				got = got[:100]
			}
			if len(want) > 100 {
				want = want[:100]
			}
			return nil, nil, fmt.Errorf("pin output mismatch: expected %q got %q", want, got)
		}
		counts = append(counts, float64(count))
		if alloc != nil {
			allocs = append(allocs, float64(*alloc))
		}
	}
	summary := &CaseSummary{PinInstructions: SummarizeNumbers(counts)}
	if allocShim != "" {
		if len(allocs) != pinRepeat {
			return nil, nil, errors.New("pin alloc output unreadable: missing shim total")
		}
		summary.AllocatedBytes = SummarizeNumbers(allocs)
	} else if len(allocs) == pinRepeat && len(allocs) > 0 {
		summary.AllocatedBytes = SummarizeNumbers(allocs)
	}
	return summary, nil, nil
}
