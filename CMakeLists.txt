cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)

set(CRUNCH_PROJECT_NAME crunch)
set(CRUNCH_LIBRARY_NAME crn)
set(CRUNCH_EXE_NAME crunch)

project(${CRUNCH_PROJECT_NAME})

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

if (NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE "Release" CACHE
		STRING "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel" FORCE)
endif()

find_package(Git)

if (Git_FOUND)
  execute_process(
    COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
  )

  if (GIT_VERSION)
    add_definitions(-DCOMPUTED_VERSION_SUFFIX="Built from git-${GIT_VERSION}")
  endif()
endif()

macro(set_cxx_flag FLAG)
	if (${ARGC} GREATER 1)
		set(CMAKE_CXX_FLAGS_${ARGV1} "${CMAKE_CXX_FLAGS_${ARGV1}} ${FLAG}")
	else()
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${FLAG}")
	endif()
endmacro()

macro(set_linker_flag FLAG)
	if (${ARGC} GREATER 1)
		set(CMAKE_EXE_LINKER_FLAGS_${ARGV1} "${CMAKE_EXE_LINKER_FLAGS_${ARGV1}} ${FLAG}")
		set(CMAKE_SHARED_LINKER_FLAGS_${ARGV1} "${CMAKE_SHARED_LINKER_FLAGS_${ARGV1}} ${FLAG}")
		set(CMAKE_MODULE_LINKER_FLAGS_${ARGV1} "${CMAKE_MODULE_LINKER_FLAGS_${ARGV1}} ${FLAG}")
	else()
		set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${FLAG}")
		set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} ${FLAG}")
		set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} ${FLAG}")
	endif()
endmacro()

# This option decides if crunch is dynamically linked against libcrn.so
# statically linked against libcrn.o, enabling it always build libcrn.so.
# This option is a builtin CMake one, the name means “build executables
# against shader libraries”, not “build the shared libraries”.
option(BUILD_SHARED_LIBS "Link executables against shared library" OFF)
# Always build libcrn.so even if crunch is linked to libcrn statically.
option(BUILD_SHARED_LIBCRN "Build shared libcrn" OFF)
# Always build libcrn.a even if crunch is linked to libcrn dynamically.
option(BUILD_STATIC_LIBCRN "Build static libcrn" OFF)
# Build the crunch tool, implies the build of libcrn.o or libcrn.so.
option(BUILD_CRUNCH "Build crunch" ON)
# Build the provided examples, they only build on Windows for now.
option(BUILD_EXAMPLES "Build examples" OFF)
# Enable extra optimization flags, like using -O3 even in RelWithDebInfo build.
option(USE_EXTRA_OPTIMIZATION "Enable extra optimization" ON)
# Enable link time optimization, slows down the build but produce faster and smaller binaries.
option(USE_LTO "Enable link-time optimization" ON)
# Enabling fast math makes generated images less likely to be reproducible.
# See https://github.com/DaemonEngine/crunch/issues/29
option(USE_FAST_MATH "Enable fast math (generated images are less likely to be reproducible)" ON)

if (MSVC)
	# Enable MSVC parallel compilation.
	set_cxx_flag("/MP")

	# MSVC doesn't implement strict aliasing so there is nothing else to do.
	
	# CMake already sets the /O2 flag on Release and RelWithDebInfo build and /O[1-2] already sets the /Oy flag.

	if (USE_FAST_MATH)
		set_cxx_flag("/fp:fast")
	endif()

	if (USE_LTO)
		set_cxx_flag("/GL" RELEASE)
		set_cxx_flag("/GL" RELWITHDEBINFO)
		set_cxx_flag("/GL" MINSIZEREL)
		set_linker_flag("/LTCG" RELEASE)
		set_linker_flag("/LTCG" RELWITHDEBINFO)
		set_linker_flag("/LTCG" MINSIZEREL)
	endif()
else()
	# As written in crnlib.h and stb_image.h, strict aliasing should always be disabled.
	set_cxx_flag("-fno-strict-aliasing")

	# Generate maxmimum amount of debug information, including macro definitions.
	set_cxx_flag("-g3" DEBUG)
	set_cxx_flag("-g3" RELWITHDEBINFO)

	if (USE_EXTRA_OPTIMIZATION)
		# CMake already sets the -O3 flag on Release build and -O[1-3s] already sets the -fomit-frame-pointer flag.
		set_cxx_flag("-Og" DEBUG)
		set_cxx_flag("-O3" RELWITHDEBINFO)
	endif()

	if (USE_FAST_MATH)
		set_cxx_flag("-ffast-math -fno-math-errno")
	endif()

	# It should be done at the very end because it copies all compiler flags
	# to the linker flags.
	if (USE_LTO)
		set_cxx_flag("-flto" RELEASE)
		set_cxx_flag("-flto" RELWITHDEBINFO)
		set_cxx_flag("-flto" MINSIZEREL)
		set_linker_flag("${CMAKE_CXX_FLAGS}" RELEASE)
		set_linker_flag("${CMAKE_CXX_FLAGS}" RELWITHDEBINFO)
		set_linker_flag("${CMAKE_CXX_FLAGS}" MINSIZEREL)
	endif()
endif()

if (BUILD_SHARED_LIBCRN OR BUILD_STATIC_LIBCRN OR BUILD_CRUNCH)
  add_subdirectory(crnlib crnlib)
endif()

if (BUILD_CRUNCH)
  add_subdirectory(crunch _crunch)
endif()

if(BUILD_EXAMPLES)
  add_subdirectory(example1 _example1)
  add_subdirectory(example2 _example2)
  add_subdirectory(example3 _example3)
endif()
