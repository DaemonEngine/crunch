/* 7zBuf.c -- Byte Buffer
2008-03-28
Igor Pavlov
Public domain */
#include "crn_core.h"

#include "lzma_7zBuf.h"

namespace crnlib {

void Buf_Init(CBuf* p) {
  p->data = nullptr;
  p->size = 0;
}

int Buf_Create(CBuf* p, size_t size, ISzAlloc* alloc) {
  p->size = 0;
  if (size == 0) {
    p->data = nullptr;
    return 1;
  }
  p->data = (Byte*)alloc->Alloc(alloc, size);
  if (p->data != nullptr) {
    p->size = size;
    return 1;
  }
  return 0;
}

void Buf_Free(CBuf* p, ISzAlloc* alloc) {
  alloc->Free(alloc, p->data);
  p->data = nullptr;
  p->size = 0;
}
}
