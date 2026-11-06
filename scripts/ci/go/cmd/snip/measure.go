package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync"
	"time"

	"github.com/hhh-pa/python-code-snippet/scripts/ci/go/internal/measure"
	"github.com/hhh-pa/python-code-snippet/scripts/ci/go/internal/snipcore"
)

const measureUsage = `Load-independent performance measurement for Python snippets.

Runs every src/**/*.py script against the shared test cases --repeat
times via python3, gating correctness on stdout, and records CPU time
and peak RSS from wait4 rusage. With --callgrind the timed phase runs
under Valgrind Callgrind and records simulated instruction reads (Ir)
too (CPU/RSS then describe the valgrind process, tool overhead
included); with the pin flags each case is also measured under Pin,
yielding instruction counts plus allocated bytes from an inscount
tool run with an LD_PRELOAD allocation shim in the same run.

--repeat 0 selects the pin-only mode: no timed phase runs, and each case
is measured once under Pin, which yields pin_instructions together with
allocated_bytes (parsed from the run's stderr) while still gating
correctness on the Pin run's stdout. Reports carry Runs 0 with no
time/memory summaries; the BMF and summary table omit cpu_time
rather than emitting zeros.

allocated_bytes is cumulative libc allocation for the whole process run
(freed bytes never subtracted). It INCLUDES Pin's own JIT/VM
allocations, so like pin_instructions it is only comparable within one
Pin version. Peak RSS under Pin is NOT meaningful: maxrss is never
read from instrumented runs and stays null in pin-only sweeps.

Usage:
  snip measure [--resources DIR] [--repeat N] [--jobs N] [--timeout S]
               [--only SUBSTR] [--shard K/N] [--output JSON]
               [--bmf-output JSON] [--summary-file MD] [--callgrind]
               [--pin] [--pin-bin BIN] [--pin-tool SO] [--pin-repeat N]
               [--pin-timeout S]

  snip measure --merge shard-*.json [--output JSON] [--bmf-output JSON]
               [--summary-file MD]

  snip measure --self-test

Report comparison lives in snip compare.
`

type measureTask struct {
	label    string
	stem     string
	script   string
	caseName string
	inp      string
	outp     string
}

func runMeasure(argv []string) int {
	root := snipcore.RepoRoot()
	resources := filepath.Join(root, "tests", "resources")
	jobs := 2
	repeat := 1
	timeout := 300
	pinRepeat := measure.PinRepeatDefault
	pinTimeout := 600
	var only, shard, output, bmfOutput, summaryFile, mergeFilesStr, pinBin, pinTool string
	var selfTest, pin, callgrind bool

	// Parse flags manually or with flagSpec; note that --merge can take multiple files.
	// We extract --merge and --self-test first if present.
	var remaining []string
	var mergePaths []string
	isMerge := false

	for i := 0; i < len(argv); i++ {
		arg := argv[i]
		if arg == "--self-test" {
			selfTest = true
		} else if arg == "--merge" {
			isMerge = true
			for i+1 < len(argv) && !strings.HasPrefix(argv[i+1], "-") {
				i++
				mergePaths = append(mergePaths, argv[i])
			}
		} else {
			remaining = append(remaining, arg)
		}
	}

	_, err := parseFlags("measure", remaining, flagSpec{
		Strs: map[string]*string{
			"resources":    &resources,
			"only":         &only,
			"shard":        &shard,
			"output":       &output,
			"bmf-output":   &bmfOutput,
			"summary-file": &summaryFile,
			"merge":        &mergeFilesStr,
			"pin-bin":      &pinBin,
			"pin-tool":     &pinTool,
		},
		Ints: map[string]*int{
			"jobs":        &jobs,
			"repeat":      &repeat,
			"timeout":     &timeout,
			"pin-repeat":  &pinRepeat,
			"pin-timeout": &pinTimeout,
		},
		Bools: map[string]*bool{
			"self-test": &selfTest,
			"pin":       &pin,
			"callgrind": &callgrind,
		},
	})
	if err != nil {
		if errors.Is(err, errHelp) {
			fmt.Print(measureUsage)
			return 0
		}
		fmt.Fprintln(os.Stderr, err)
		return 2
	}

	if jobs < 1 {
		fmt.Fprintln(os.Stderr, "snip measure: --jobs must be >= 1")
		return 2
	}
	if repeat < 0 {
		fmt.Fprintln(os.Stderr, "snip measure: --repeat must be >= 0")
		return 2
	}
	if pinRepeat < 1 {
		fmt.Fprintln(os.Stderr, "snip measure: --pin-repeat must be >= 1")
		return 2
	}
	if pinTimeout < 1 {
		fmt.Fprintln(os.Stderr, "snip measure: --pin-timeout must be >= 1")
		return 2
	}

	if selfTest {
		return runSelfTest()
	}

	if isMerge || mergeFilesStr != "" {
		if mergeFilesStr != "" {
			mergePaths = append(mergePaths, strings.Fields(mergeFilesStr)...)
		}
		rep, bmf, err := measure.MergeReports(mergePaths)
		if err != nil {
			fmt.Fprintf(os.Stderr, "snip measure merge: %v\n", err)
			return 1
		}
		if output != "" {
			data, _ := json.MarshalIndent(rep, "", "  ")
			if err := os.WriteFile(output, data, 0o666); err != nil {
				fmt.Fprintf(os.Stderr, "write %s: %v\n", output, err)
				return 1
			}
		}
		if bmfOutput != "" {
			data, _ := json.MarshalIndent(bmf, "", "  ")
			if err := os.WriteFile(bmfOutput, data, 0o666); err != nil {
				fmt.Fprintf(os.Stderr, "write %s: %v\n", bmfOutput, err)
				return 1
			}
		}
		if summaryFile != "" {
			if err := measure.AppendSummary(summaryFile, rep, bmf); err != nil {
				fmt.Fprintf(os.Stderr, "append summary: %v\n", err)
			}
		}
		fmt.Printf("Merged %d reports: %d cases, %d benchmarks.\n", len(mergePaths), len(rep.Results), len(bmf))
		return 0
	}

	_, valgrindErr := exec.LookPath("valgrind")
	hasValgrind := callgrind && valgrindErr == nil
	if callgrind && valgrindErr != nil {
		fmt.Fprintln(os.Stderr, "snip measure: --callgrind needs valgrind on PATH")
		return 1
	}

	usePin := pin && measure.PinUsable(pinBin, pinTool)
	if pin && !usePin {
		fmt.Fprintln(os.Stderr, "snip measure: --pin needs a usable kit (--pin-bin launcher and --pin-tool inscount .so)")
		return 1
	}
	var pinVersion *string
	if usePin {
		pinVersion = measure.PinVersion(pinBin)
	}
	effectivePin := 0
	if usePin {
		effectivePin = pinRepeat
	}
	if repeat == 0 && effectivePin == 0 {
		fmt.Fprintln(os.Stderr, "snip measure: --repeat 0 needs a measurement phase (--pin with a usable kit and tool)")
		return 2
	}

	// Build the LD_PRELOAD alloc shim on demand so the Pin run
	// yields allocated_bytes alongside pin_instructions. A missing
	// shim degrades to pin_instructions-only (warning, not an
	// error); a built shim that yields no total fails the case in
	// the Pin phase below (harness broken, not the snippet).
	allocShim := ""
	if effectivePin > 0 {
		var shimErr error
		allocShim, shimErr = measure.EnsureAllocShim(root)
		if shimErr != nil {
			fmt.Fprintf(os.Stderr, "warning: alloc shim unavailable (%v); allocated_bytes will be null\n", shimErr)
			allocShim = ""
		}
	}

	python := pythonBin()

	found, err := snipcore.Discover(root, resources)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 1
	}

	var tasks []measureTask
	var missing []string
	for _, entry := range found {
		label := entry.Label
		if only != "" && !strings.Contains(label, only) && !strings.Contains(entry.Script, only) {
			continue
		}
		if len(entry.Cases) == 0 {
			// No --only filter: a caseless snippet is missing
			// resources and fails the sweep like `snip test`.
			if only == "" {
				missing = append(missing, label)
			}
			continue
		}
		for _, c := range entry.Cases {
			tasks = append(tasks, measureTask{
				label:    label,
				stem:     entry.Stem,
				script:   entry.Script,
				caseName: c.Name,
				inp:      c.Input,
				outp:     c.Output,
			})
		}
	}

	sort.Slice(tasks, func(i, j int) bool {
		if tasks[i].label != tasks[j].label {
			return tasks[i].label < tasks[j].label
		}
		return tasks[i].caseName < tasks[j].caseName
	})

	// Shard by snippet label (cohesive sharding, shared with snip test)
	shardIndex, shardTotal := 0, 1
	if shard != "" {
		var shardErr error
		shardIndex, shardTotal, shardErr = snipcore.ParseShard(shard)
		if shardErr != nil {
			fmt.Fprintln(os.Stderr, shardErr)
			return 1
		}
		tasks = snipcore.FilterShard(tasks, func(t measureTask) string { return t.label }, shardIndex, shardTotal)
	}

	totalTasks := len(tasks)
	benchSet := map[string]bool{}
	neededScriptsSet := map[string]bool{}
	for _, t := range tasks {
		benchSet[t.label] = true
		neededScriptsSet[t.script] = true
	}
	var neededScripts []string
	for s := range neededScriptsSet {
		neededScripts = append(neededScripts, s)
	}
	sort.Strings(neededScripts)

	fmt.Printf("Measuring %d cases (%d benchmarks, %d snippets)...\n", totalTasks, len(benchSet), len(neededScripts))

	var results []measure.CaseResult
	var failures []string
	// Missing labels are shard-scoped like tasks: each shard reports
	// only its own, so the merged failures list carries no duplicates.
	scopedMissing := missing
	if shard != "" {
		scopedMissing = snipcore.FilterShard(missing, func(s string) string { return s }, shardIndex, shardTotal)
	}
	for _, label := range scopedMissing {
		failures = append(failures, fmt.Sprintf("%s: no resources found", label))
	}
	done := 0

	sem := make(chan struct{}, jobs)
	var wg sync.WaitGroup
	var mu sync.Mutex

	for _, t := range tasks {
		cmd := []string{python, t.script}

		wg.Add(1)
		go func(tk measureTask, runCmd []string) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()

			var summary *measure.CaseSummary
			var measErr error
			if repeat > 0 {
				summary, measErr = measure.MeasureCaseCallgrind(hasValgrind, runCmd, tk.inp, tk.outp, repeat, timeout)
			} else {
				// Pin-only: no timed phase; the Pin phase below
				// hangs its signals on this shell (Runs stays 0).
				summary = &measure.CaseSummary{Runs: 0}
			}
			var pinSkipped *string
			if measErr == nil && effectivePin > 0 {
				var pinSummary *measure.CaseSummary
				pinSummary, pinSkipped, measErr = measure.MeasureCasePin(
					tk.label, tk.caseName, runCmd, tk.inp, tk.outp,
					pinBin, pinTool, effectivePin, pinTimeout, allocShim)
				if measErr == nil && pinSummary != nil {
					summary.PinInstructions = pinSummary.PinInstructions
					summary.AllocatedBytes = pinSummary.AllocatedBytes
				}
			}

			mu.Lock()
			done++
			if measErr == nil {
				insnStr := "n/a"
				if summary.Instructions != nil {
					insnStr = fmt.Sprintf("%s Ir", formatInt(int64(summary.Instructions.Median)))
				}
				pinInfo := ""
				if summary.PinInstructions != nil {
					pinInfo = fmt.Sprintf("; %s Pin", formatInt(int64(summary.PinInstructions.Median)))
				} else if pinSkipped != nil {
					pinInfo = fmt.Sprintf(" (pin skipped: %s)", *pinSkipped)
				}
				if summary.AllocatedBytes != nil {
					pinInfo += fmt.Sprintf("; %sB alloc", formatInt(int64(summary.AllocatedBytes.Median)))
				}
				fmt.Printf("[%d/%d] %s/%s: %s%s\n", done, totalTasks, tk.label, tk.caseName, insnStr, pinInfo)
				relScript, _ := filepath.Rel(root, tk.script)
				results = append(results, measure.CaseResult{
					Label:      tk.label,
					Stem:       tk.stem,
					Case:       tk.caseName,
					Script:     filepath.ToSlash(relScript),
					Summary:    summary,
					PinSkipped: pinSkipped,
				})
			} else {
				fmt.Printf("[%d/%d] FAIL %s/%s: %v\n", done, totalTasks, tk.label, tk.caseName, measErr)
				failures = append(failures, fmt.Sprintf("%s/%s: %v", tk.label, tk.caseName, measErr))
			}
			mu.Unlock()
		}(t, cmd)
	}
	wg.Wait()

	sort.Slice(results, func(i, j int) bool {
		if results[i].Label != results[j].Label {
			return results[i].Label < results[j].Label
		}
		return results[i].Case < results[j].Case
	})

	rep := &measure.Report{
		ToolVersion: measure.ToolVersion,
		Platform:    runtime.GOOS + "/" + runtime.GOARCH,
		Date:        time.Now().UTC().Format(time.RFC3339),
		HasValgrind: hasValgrind,
		PinUsed:     usePin,
		PinVersion:  pinVersion,
		Results:     results,
		Failures:    failures,
	}
	bmf := measure.BuildBMF(results)

	if output != "" {
		data, _ := json.MarshalIndent(rep, "", "  ")
		_ = os.WriteFile(output, data, 0o666)
	}
	if bmfOutput != "" {
		data, _ := json.MarshalIndent(bmf, "", "  ")
		_ = os.WriteFile(bmfOutput, data, 0o666)
	}
	if summaryFile != "" {
		_ = measure.AppendSummary(summaryFile, rep, bmf)
	}

	if len(failures) > 0 {
		return 1
	}
	return 0
}

func formatInt(n int64) string {
	in := fmt.Sprintf("%d", n)
	var out []byte
	l := len(in)
	for i := 0; i < l; i++ {
		if i > 0 && (l-i)%3 == 0 {
			out = append(out, ',')
		}
		out = append(out, in[i])
	}
	return string(out)
}

func runSelfTest() int {
	fmt.Println("Running self-test for snip measure...")

	sampleCg := `
events: Ir
summary: 987654321
totals: 987654321
`
	parsed, err := measure.ParseCallgrindOutput(sampleCg)
	if err != nil || parsed != 987654321 {
		fmt.Fprintf(os.Stderr, "ParseCallgrindOutput: expected 987654321, got %d, err: %v\n", parsed, err)
		return 1
	}

	if n, err := measure.ParsePinCount("Count 846018869\n"); err != nil || n != 846018869 {
		fmt.Fprintf(os.Stderr, "ParsePinCount: expected 846018869, got %d, err: %v\n", n, err)
		return 1
	}
	if n, err := measure.ParsePinCount("Pin 3.31\nCount 1\nCount 42\n"); err != nil || n != 42 {
		fmt.Fprintf(os.Stderr, "ParsePinCount: later Count must win, got %d, err: %v\n", n, err)
		return 1
	}
	for _, bad := range []string{"", "no counts here\n", "Count abc\n", "Count\n", "Count 1 2\n"} {
		if n, err := measure.ParsePinCount(bad); err == nil {
			fmt.Fprintf(os.Stderr, "ParsePinCount: must reject %q, got %d\n", bad, n)
			return 1
		}
	}

	if n, found := measure.ParseAllocBytes("noise\nsnip_alloc_total_bytes=12345\n"); !found || n != 12345 {
		fmt.Fprintf(os.Stderr, "ParseAllocBytes: expected (12345, true), got (%d, %v)\n", n, found)
		return 1
	}
	if n, found := measure.ParseAllocBytes("snip_alloc_total_bytes=1\nsnip_alloc_total_bytes=42\n"); !found || n != 42 {
		fmt.Fprintf(os.Stderr, "ParseAllocBytes: later marker must win, got (%d, %v)\n", n, found)
		return 1
	}
	for _, absent := range []string{"", "no marker here\n", "snip_alloc_total_bytes=abc\n", "snip_alloc_total_bytes=\n", "snip_alloc_total_bytes=-5\n"} {
		if n, found := measure.ParseAllocBytes("snippet stderr\n" + absent); found {
			fmt.Fprintf(os.Stderr, "ParseAllocBytes: must not match %q, got %d\n", absent, n)
			return 1
		}
	}

	mockResults := []measure.CaseResult{
		{
			Label: "sort/merge_sort",
			Case:  "tc0",
			Summary: &measure.CaseSummary{
				Instructions:    &measure.NumberSummary{Median: 1000},
				PinInstructions: &measure.NumberSummary{Median: 5000},
				AllocatedBytes:  &measure.NumberSummary{Median: 800},
				CpuS:            &measure.NumberSummary{Median: 0.05},
			},
		},
		{
			Label: "sort/merge_sort",
			Case:  "tc1",
			Summary: &measure.CaseSummary{
				Instructions:    &measure.NumberSummary{Median: 2000},
				PinInstructions: &measure.NumberSummary{Median: 7000},
				AllocatedBytes:  &measure.NumberSummary{Median: 1200},
				CpuS:            &measure.NumberSummary{Median: 0.05},
			},
		},
	}
	bmf := measure.BuildBMF(mockResults)
	m := bmf["sort/merge_sort"]
	if m.Instructions == nil || m.Instructions.Value.(int64) != 3000 {
		fmt.Fprintf(os.Stderr, "BMF instructions: expected 3000, got %v\n", m.Instructions)
		return 1
	}
	if m.PinInstructions == nil || m.PinInstructions.Value.(int64) != 12000 {
		fmt.Fprintf(os.Stderr, "BMF pin_instructions: expected 12000, got %v\n", m.PinInstructions)
		return 1
	}
	if m.AllocatedBytes == nil || m.AllocatedBytes.Value.(int64) != 2000 {
		fmt.Fprintf(os.Stderr, "BMF allocated_bytes: expected 2000, got %v\n", m.AllocatedBytes)
		return 1
	}
	if m.CpuTime == nil || math.Abs(m.CpuTime.Value.(float64)-0.10) > 1e-6 {
		fmt.Fprintf(os.Stderr, "BMF cpu_time: expected 0.10, got %v\n", m.CpuTime)
		return 1
	}

	pinOnly := []measure.CaseResult{
		{
			Label: "sort/merge_sort",
			Case:  "tc0",
			Summary: &measure.CaseSummary{
				Runs:            0,
				PinInstructions: &measure.NumberSummary{Median: 5000},
				AllocatedBytes:  &measure.NumberSummary{Median: 800},
			},
		},
	}
	pm := measure.BuildBMF(pinOnly)["sort/merge_sort"]
	if pm.CpuTime != nil {
		fmt.Fprintf(os.Stderr, "BMF pin-only: cpu_time must be omitted, got %v\n", pm.CpuTime)
		return 1
	}
	if pm.PinInstructions == nil || pm.PinInstructions.Value.(int64) != 5000 {
		fmt.Fprintf(os.Stderr, "BMF pin-only: pin_instructions expected 5000, got %v\n", pm.PinInstructions)
		return 1
	}
	if pm.AllocatedBytes == nil || pm.AllocatedBytes.Value.(int64) != 800 {
		fmt.Fprintf(os.Stderr, "BMF pin-only: allocated_bytes expected 800, got %v\n", pm.AllocatedBytes)
		return 1
	}

	// Alloc-shim build + smoke (Linux only: LD_PRELOAD
	// interposition has no macOS equivalent). Skipped when the
	// shim source is absent (unit tests run in a temp dir, not
	// the repo root).
	if runtime.GOOS == "linux" {
		shimSrc := filepath.Join(snipcore.RepoRoot(), "scripts", "ci", "instrumentation", "allocshim.c")
		if _, err := os.Stat(shimSrc); err != nil {
			fmt.Println("(skipping alloc-shim build test: source not present)")
		} else {
			shim, shimErr := measure.EnsureAllocShim(snipcore.RepoRoot())
			if shimErr != nil {
				fmt.Fprintf(os.Stderr, "EnsureAllocShim: %v\n", shimErr)
				return 1
			}
			if _, err := os.Stat(shim); err != nil {
				fmt.Fprintf(os.Stderr, "shim missing at %s\n", shim)
				return 1
			}
			prev := os.Getenv("LD_PRELOAD")
			preload := shim
			if prev != "" {
				preload = shim + ":" + prev
			}
			_, stderr, runErr := snipcore.RunEnv(
				[]string{pythonBin(), "-c", "print('hi')"}, nil, 60,
				[]string{"LD_PRELOAD=" + preload})
			if runErr != nil {
				fmt.Fprintf(os.Stderr, "shim smoke run: %v (%s)\n", runErr, string(stderr))
				return 1
			}
			total, found := measure.ParseAllocBytes(string(stderr))
			if !found || total <= 0 {
				fmt.Fprintf(os.Stderr, "shim smoke: expected total > 0, got (%d, %v)\n", total, found)
				return 1
			}
		}
	} else {
		fmt.Println("(skipping alloc-shim build test: needs Linux)")
	}

	fmt.Println("self-test passed!")
	return 0
}
