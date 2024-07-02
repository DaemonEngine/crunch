.DEFAULT_GOAL := all
.PHONY: all clean

CXX = emcc

COMPILE_OPTIMIZATION_OPTIONS = -O3
COMPILE_OPTIONS = -std=c++11 ${COMPILE_OPTIMIZATION_OPTIONS}

LINKER_OPTIONS = -s EXPORTED_FUNCTIONS="['_malloc', '_free', '_crn_get_width', '_crn_get_height', '_crn_get_levels', '_crn_get_dxt_format', '_crn_get_bytes_per_block', '_crn_get_uncompressed_size', '_crn_decompress']" -s NO_EXIT_RUNTIME=1 -s NO_FILESYSTEM=1 -s ELIMINATE_DUPLICATE_FUNCTIONS=1 -s ALLOW_MEMORY_GROWTH=1 --memory-init-file 0

all: crunch.js

crunch.js: crunch_lib.cpp
	$(CXX) $< -o $@ -I../inc $(COMPILE_OPTIONS) $(LINKER_OPTIONS)

clean:
	rm crunch.js crunch.wasm
