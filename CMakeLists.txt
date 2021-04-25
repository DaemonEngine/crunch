cmake_minimum_required(VERSION 3.1)

set(CRUNCH_PROJECT_NAME crunch)
set(CRUNCH_LIBRARY_NAME crn)
set(CRUNCH_EXE_NAME crunch)

project(${CRUNCH_PROJECT_NAME})

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

option(BUILD_SHARED_LIBS "Link executables against shared library" OFF)
option(BUILD_EXAMPLES "Build examples" OFF)
option(INSTALL_CRNLIB "Install crnlib" OFF)
option(OPTIMIZE_RELEASE "Optimize release build" ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wno-unused-value -Wno-unused")

if(OPTIMIZE_RELEASE)
  # CMake already sets -O3 flag on release build
  set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fomit-frame-pointer -ffast-math -fno-math-errno -fno-strict-aliasing")
endif()

if(BUILD_EXAMPLES)
  add_subdirectory(example1 _example1)
  add_subdirectory(example2 _example2)
  add_subdirectory(example3 _example3)
endif()

add_subdirectory(crnlib)

add_subdirectory(crunch _crunch)
