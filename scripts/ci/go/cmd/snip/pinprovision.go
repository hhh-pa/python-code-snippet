package main

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/hhh-pa/python-code-snippet/scripts/ci/go/internal/snipcore"
)

const pinProvisionUsage = `Provision Intel Pin 4.4 + the vendored inscount tool for local
snip measure --pin runs.

Idempotent: when the instrumentation dir already holds a kit and a
built tool, it just re-exports the paths. Otherwise it downloads
the kit from Intel, verifies its sha256, extracts it, and builds
scripts/ci/instrumentation/inscount.cpp against it.
snip measure builds scripts/ci/instrumentation/allocshim.c on
demand with cc at sweep time.

CI does NOT use this subcommand (it uses .github/actions/pin-tools,
which duplicates the PIN_URL/PIN_SHA256 below — bump both
together).

Outputs (stdout for logs, $GITHUB_ENV when present):
  INSTRUMENTATION_BIN   absolute path to the pin launcher
  INSTRUMENTATION_TOOL  absolute path to obj-intel64/inscount.so

Usage: snip pin-provision [--dir DIR]

--dir overrides $INSTRUMENTATION_DIR (default $HOME/instrumentation).
$PIN_URL and $PIN_SHA256 override the kit URL and checksum.
`

const (
	pinURL    = "https://software.intel.com/sites/landingpage/pintool/downloads/pin-external-4.4-99977-g54fbb8814-gcc-linux.tar.gz"
	pinSHA256 = "3138183a5d2b51ea5c8f29edd148b67ac9c249e2c510cc0e9e2a5880f523a34c"
	pinTopDir = "pin-external-4.4-99977-g54fbb8814-gcc-linux"
)

func runPinProvision(argv []string) int {
	var dirFlag string
	_, err := parseFlags("pin-provision", argv, flagSpec{
		Strs: map[string]*string{"dir": &dirFlag},
	})
	if err != nil {
		if errors.Is(err, errHelp) {
			fmt.Print(pinProvisionUsage)
			return 0
		}
		fmt.Fprintln(os.Stderr, err)
		return 2
	}

	url := os.Getenv("PIN_URL")
	if url == "" {
		url = pinURL
	}
	wantSHA := os.Getenv("PIN_SHA256")
	if wantSHA == "" {
		wantSHA = pinSHA256
	}
	instDir := dirFlag
	if instDir == "" {
		instDir = os.Getenv("INSTRUMENTATION_DIR")
	}
	if instDir == "" {
		home, herr := os.UserHomeDir()
		if herr != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision: cannot resolve home dir:", herr)
			return 1
		}
		instDir = filepath.Join(home, "instrumentation")
	}

	root := snipcore.RepoRoot()
	toolSrc := filepath.Join(root, "scripts", "ci", "instrumentation")
	kitDir := filepath.Join(instDir, pinTopDir)
	pinBin := filepath.Join(kitDir, "pin")
	toolBuild := filepath.Join(instDir, "toolbuild")
	pinTool := filepath.Join(toolBuild, "obj-intel64", "inscount.so")

	needTool := !isExecutable(pinBin) || !fileExists(pinTool)
	if needTool {
		if _, err := exec.LookPath("g++"); err != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision: g++ is required to build the inscount tool")
			return 1
		}
		if _, err := exec.LookPath("make"); err != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision: make is required to build the inscount tool")
			return 1
		}
		if !fileExists(filepath.Join(toolSrc, "inscount.cpp")) {
			fmt.Fprintf(os.Stderr, "snip pin-provision: tool sources missing at %s\n", toolSrc)
			return 1
		}
		if !fileExists(filepath.Join(toolSrc, "allocshim.c")) {
			fmt.Fprintf(os.Stderr, "snip pin-provision: alloc-shim source missing at %s\n", toolSrc)
			return 1
		}
		if err := os.MkdirAll(instDir, 0o755); err != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision:", err)
			return 1
		}
		if !isExecutable(pinBin) {
			fmt.Fprintln(os.Stderr, "snip pin-provision: downloading Pin 4.4 kit...")
			kitTar := filepath.Join(instDir, "pin-kit.tar.gz")
			if derr := downloadWithRetry(url, kitTar); derr != nil {
				fmt.Fprintln(os.Stderr, "snip pin-provision:", derr)
				return 1
			}
			if serr := verifySHA256(kitTar, wantSHA); serr != nil {
				fmt.Fprintln(os.Stderr, "snip pin-provision:", serr)
				return 1
			}
			tarBin, terr := exec.LookPath("tar")
			if terr != nil {
				fmt.Fprintln(os.Stderr, "snip pin-provision: tar is required to extract the Pin kit")
				return 1
			}
			stdout, stderr, runErr := snipcore.Run(
				[]string{tarBin, "xzf", kitTar, "-C", instDir}, nil, 600)
			_ = stdout
			if runErr != nil {
				fmt.Fprintf(os.Stderr, "snip pin-provision: extract failed: %v (%s)\n", runErr, strings.TrimSpace(string(stderr)))
				return 1
			}
			_ = os.Remove(kitTar)
		}
		fmt.Fprintln(os.Stderr, "snip pin-provision: building inscount tool...")
		_ = os.RemoveAll(toolBuild)
		if err := os.MkdirAll(toolBuild, 0o755); err != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision:", err)
			return 1
		}
		for _, name := range []string{"inscount.cpp", "makefile", "makefile.rules"} {
			data, rerr := os.ReadFile(filepath.Join(toolSrc, name))
			if rerr != nil {
				fmt.Fprintln(os.Stderr, "snip pin-provision:", rerr)
				return 1
			}
			if werr := os.WriteFile(filepath.Join(toolBuild, name), data, 0o666); werr != nil {
				fmt.Fprintln(os.Stderr, "snip pin-provision:", werr)
				return 1
			}
		}
		logFile, lerr := os.CreateTemp("", "instrumentation-tool-build-*.log")
		if lerr != nil {
			fmt.Fprintln(os.Stderr, "snip pin-provision:", lerr)
			return 1
		}
		logPath := logFile.Name()
		_ = logFile.Close()
		makeBin, _ := exec.LookPath("make")
		stdout, stderr, runErr := snipcore.RunCwd(
			[]string{makeBin, "-C", toolBuild, "PIN_ROOT=" + kitDir}, nil, toolBuild, 600)
		combined := append(stdout, stderr...)
		_ = os.WriteFile(logPath, combined, 0o666)
		if runErr != nil {
			lines := strings.Split(strings.TrimSpace(string(combined)), "\n")
			start := 0
			if len(lines) > 20 {
				start = len(lines) - 20
			}
			for _, ln := range lines[start:] {
				fmt.Fprintln(os.Stderr, ln)
			}
			fmt.Fprintln(os.Stderr, "snip pin-provision: tool build failed")
			return 1
		}
	}

	if !isExecutable(pinBin) {
		fmt.Fprintf(os.Stderr, "snip pin-provision: pin launcher missing at %s\n", pinBin)
		return 1
	}
	if !fileExists(pinTool) {
		fmt.Fprintf(os.Stderr, "snip pin-provision: tool missing at %s\n", pinTool)
		return 1
	}
	if _, _, verr := snipcore.Run([]string{pinBin, "-version"}, nil, 60); verr != nil {
		fmt.Fprintln(os.Stderr, "snip pin-provision: pin launcher does not run")
		return 1
	}

	fmt.Printf("INSTRUMENTATION_BIN=%s\n", pinBin)
	fmt.Printf("INSTRUMENTATION_TOOL=%s\n", pinTool)
	if envFile := os.Getenv("GITHUB_ENV"); envFile != "" {
		f, ferr := os.OpenFile(envFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o666)
		if ferr == nil {
			fmt.Fprintf(f, "INSTRUMENTATION_BIN=%s\n", pinBin)
			fmt.Fprintf(f, "INSTRUMENTATION_TOOL=%s\n", pinTool)
			_ = f.Close()
		}
	}
	return 0
}

func isExecutable(path string) bool {
	info, err := os.Stat(path)
	return err == nil && !info.IsDir() && info.Mode()&0o111 != 0
}

func downloadWithRetry(url, dest string) error {
	client := &http.Client{Timeout: 600 * time.Second}
	var lastErr error
	for attempt := 1; attempt <= 3; attempt++ {
		if err := downloadOnce(client, url, dest); err != nil {
			lastErr = err
			continue
		}
		return nil
	}
	return fmt.Errorf("download %s: %v", url, lastErr)
}

func downloadOnce(client *http.Client, url, dest string) error {
	resp, err := client.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("HTTP %s", resp.Status)
	}
	out, err := os.Create(dest)
	if err != nil {
		return err
	}
	_, copyErr := io.Copy(out, resp.Body)
	closeErr := out.Close()
	if copyErr != nil {
		return copyErr
	}
	return closeErr
}

func verifySHA256(path, want string) error {
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	sum := sha256.Sum256(data)
	got := hex.EncodeToString(sum[:])
	if !strings.EqualFold(got, strings.TrimSpace(want)) {
		return errors.New("kit checksum mismatch")
	}
	return nil
}
