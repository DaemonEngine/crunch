cmake_minimum_required(VERSION 3.1)

set(CMAKE_CXX_STANDARD 11)

set(CRUNCH_PROJECT_NAME crunch)
set(CRUNCH_LIBRARY_NAME crn)
set(CRUNCH_EXE_NAME crunch)

project(${CRUNCH_PROJECT_NAME})

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
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

option(BUILD_SHARED_LIBS "Link executables against shared library" OFF)
option(BUILD_SHARED_LIBCRN "Build shared libcrn" OFF)
option(BUILD_STATIC_LIBCRN "Build static libcrn" OFF)
option(BUILD_CRUNCH "Build crunch" ON)
option(BUILD_EXAMPLES "Build examples" OFF)
if (NOT MSVC)
  option(OPTIMIZE_RELEASE "Optimize release build" ON)
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

if (NOT MSVC)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-unused-value -Wno-unused")
endif()

if(OPTIMIZE_RELEASE)
  # CMake already sets -O3 flag on release build
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fomit-frame-pointer -ffast-math -fno-math-errno -fno-strict-aliasing")
endif()

add_subdirectory(crnlib)

if (BUILD_CRUNCH)
  add_subdirectory(crunch _crunch)
endif()

if(BUILD_EXAMPLES)
  add_subdirectory(example1 _example1)
  add_subdirectory(example2 _example2)
  add_subdirectory(example3 _example3)
endif()
