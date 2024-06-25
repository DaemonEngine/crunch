include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc
  ${CMAKE_CURRENT_SOURCE_DIR}/../crnlib
)

# Defines the source code for the library
set(EXAMPLE1_SRCS
  ${CMAKE_CURRENT_SOURCE_DIR}/example1.cpp
)

add_executable(example1 ${EXAMPLE1_SRCS})
target_link_libraries(example1 ${CRUNCH_LIBRARY_NAME})
