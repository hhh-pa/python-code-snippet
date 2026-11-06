package main

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"github.com/hhh-pa/python-code-snippet/scripts/ci/go/internal/measure"
)

func TestEnsureAllocShimMissingSource(t *testing.T) {
	if runtime.GOOS != "linux" {
		t.Skip("shim needs Linux")
	}
	dir := t.TempDir()
	if _, err := measure.EnsureAllocShim(dir); err == nil {
		t.Fatal("missing shim source must fail")
	} else if !strings.Contains(err.Error(), "shim source missing") {
		t.Fatalf("err = %v, want shim-source-missing", err)
	}
}

func TestEnsureAllocShimBuilds(t *testing.T) {
	if runtime.GOOS != "linux" {
		t.Skip("shim needs Linux")
	}
	// Run from the repo root layout: copy the real shim source
	// into a temp repo and build it there.
	dir := t.TempDir()
	srcDir := filepath.Join(dir, "scripts", "ci", "instrumentation")
	if err := os.MkdirAll(srcDir, 0o755); err != nil {
		t.Fatal(err)
	}
	realSrc, err := filepath.Abs(filepath.Join("..", "..", "..", "instrumentation", "allocshim.c"))
	if err != nil {
		t.Fatal(err)
	}
	data, err := os.ReadFile(realSrc)
	if err != nil {
		t.Skipf("shim source not available: %v", err)
	}
	if err := os.WriteFile(filepath.Join(srcDir, "allocshim.c"), data, 0o666); err != nil {
		t.Fatal(err)
	}
	shim, err := measure.EnsureAllocShim(dir)
	if err != nil {
		t.Fatalf("EnsureAllocShim: %v", err)
	}
	if _, err := os.Stat(shim); err != nil {
		t.Fatalf("shim missing at %s: %v", shim, err)
	}
}
