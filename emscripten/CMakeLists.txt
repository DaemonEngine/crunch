cmake_minimum_required(VERSION 3.5)

set(CMAKE_CXX_STANDARD 11)

set(CRUNCHJS_EXE_NAME crunch)

if (NOT CMAKE_CXX_COMPILER)
	set(CMAKE_CXX_COMPILER emcc)
endif()

project(${CRUNCHJS_EXE_NAME}.js LANGUAGES CXX)

if (NOT CMAKE_TOOLCHAIN_FILE)
	set(CMAKE_EXECUTABLE_SUFFIX .js)
endif()

set(CMAKE_CXX_FLAGS "-O3 ${CMAKE_CXX_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -s EXPORTED_FUNCTIONS=\"['_malloc', '_free', '_crn_get_width', '_crn_get_height', '_crn_get_levels', '_crn_get_dxt_format', '_crn_get_bytes_per_block', '_crn_get_uncompressed_size', '_crn_decompress']\" -s NO_EXIT_RUNTIME=1 -s NO_FILESYSTEM=1 -s ELIMINATE_DUPLICATE_FUNCTIONS=1 -s ALLOW_MEMORY_GROWTH=1 --memory-init-file 0")

include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/../inc
)

set(CRUNCHJS_SRCS
	${CMAKE_CURRENT_SOURCE_DIR}/crunch_lib.cpp
)

add_executable(${CRUNCHJS_EXE_NAME} ${CRUNCHJS_SRCS})
