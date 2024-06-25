include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc
  ${CMAKE_CURRENT_SOURCE_DIR}/../crnlib
)

# Defines the source code for the library
set(EXAMPLE3_SRCS
  ${CMAKE_CURRENT_SOURCE_DIR}/example3.cpp
)

add_executable(example3 ${EXAMPLE3_SRCS})
target_link_libraries(example3 ${CRUNCH_LIBRARY_NAME})
