// inscount: minimal Intel Pin tool counting executed application
// instructions for the python snippet perf sweep.
//
// Instruments at TRACE/BBL granularity: each basic block gets one
// analysis call adding the block's static instruction count to a
// process-wide total (all threads, all application images; the Pin
// VM itself is never instrumented). At shutdown the tool prints a
// single line:
//
//	Count N
//
// to the file named by the -o knob (default inscount.out).
// tools/measure.py parses that line (parse_pin_count) and records
// it as pin_instructions. Build out of the kit with:
//
//	make PIN_ROOT=<kit> -C <this dir>
//
// which drops obj-intel64/inscount.so next to this file.
#include <cstdio>
#include "pin.H"

static UINT64 g_total = 0;
static FILE *g_out = nullptr;
static KNOB<std::string> KnobOut(KNOB_MODE_WRITEONCE, "pintool", "o", "inscount.out",
                                 "output file for the Count line");

static VOID AddBlock(UINT32 n) { g_total += n; }

static VOID Trace(TRACE trace, VOID *) {
	for (BBL bbl = TRACE_BblHead(trace); BBL_Valid(bbl); bbl = BBL_Next(bbl)) {
		BBL_InsertCall(bbl, IPOINT_BEFORE, (AFUNPTR)AddBlock, IARG_UINT32, BBL_NumIns(bbl),
		               IARG_END);
	}
}

static VOID Fini(INT32, VOID *) {
	if (g_out != nullptr) {
		fprintf(g_out, "Count %llu\n", (unsigned long long)g_total);
		fclose(g_out);
		g_out = nullptr;
	}
}

int main(int argc, char *argv[]) {
	PIN_InitSymbols();
	if (PIN_Init(argc, argv)) {
		return 1;
	}
	g_out = fopen(KnobOut.Value().c_str(), "w");
	if (g_out == nullptr) {
		return 1;
	}
	TRACE_AddInstrumentFunction(Trace, nullptr);
	PIN_AddFiniFunction(Fini, nullptr);
	PIN_StartProgram();
	return 0;
}
