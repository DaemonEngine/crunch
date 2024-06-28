// File: crn_platform.cpp
// See Copyright Notice and license at the end of inc/crnlib.h
#include "crn_core.h"

#if CRNLIB_USE_WIN32_API
#include "crn_winhdr.h"
#endif

#if !defined(_WIN32)
char* crnlib_strnlwr(char* p, size_t n) {
  char* q = p;
  for (size_t i = 0; i < n && *q; i++) {
    char c = *q;
    *q++ = tolower(c);
  }
  return p;
}

char* crnlib_strnupr(char* p, size_t n) {
  char* q = p;
  for (size_t i = 0; i < n && *q; i++) {
    char c = *q;
    *q++ = toupper(c);
  }
  return p;
}
#endif

void crnlib_debug_break(void) {
  CRNLIB_BREAKPOINT
}

#if CRNLIB_USE_WIN32_API
#include "crn_winhdr.h"

bool crnlib_is_debugger_present(void) {
  return IsDebuggerPresent() != 0;
}

void crnlib_output_debug_string(const char* p) {
  OutputDebugStringA(p);
}
#else
bool crnlib_is_debugger_present(void) {
  return false;
}

void crnlib_output_debug_string(const char* p) {
  puts(p);
}
#endif  // CRNLIB_USE_WIN32_API
