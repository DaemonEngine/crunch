find_package (Threads)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc
  ${CMAKE_CURRENT_SOURCE_DIR}/../crnlib
)

# Defines the source code for the library
set(CRUNCH_SRCS
  ${CMAKE_CURRENT_SOURCE_DIR}/corpus_gen.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/corpus_gen.h
  ${CMAKE_CURRENT_SOURCE_DIR}/corpus_test.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/corpus_test.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crunch.cpp
)

add_executable(${CRUNCH_EXE_NAME} ${CRUNCH_SRCS})

target_link_libraries(${CRUNCH_EXE_NAME} ${CRUNCH_LIBRARY_NAME} ${CMAKE_THREAD_LIBS_INIT})

install(TARGETS ${CRUNCH_EXE_NAME} DESTINATION bin)
set_property(TARGET ${CRUNCH_EXE_NAME} PROPERTY POSITION_INDEPENDENT_CODE 1)

if (UNIX)
    include(GNUInstallDirs)
    install(FILES crunch.1 DESTINATION ${CMAKE_INSTALL_MANDIR}/man1)
endif ()
