// File: crn_buffer_stream.h
// See Copyright Notice and license at the end of inc/crnlib.h
#pragma once
#include "crn_data_stream.h"

namespace crnlib {
class buffer_stream : public data_stream {
 public:
  buffer_stream()
      : data_stream(),
        m_pBuf(nullptr),
        m_size(0),
        m_ofs(0) {
  }

  buffer_stream(void* p, uint size)
      : data_stream(),
        m_pBuf(nullptr),
        m_size(0),
        m_ofs(0) {
    open(p, size);
  }

  buffer_stream(const void* p, uint size)
      : data_stream(),
        m_pBuf(nullptr),
        m_size(0),
        m_ofs(0) {
    open(p, size);
  }

  ~buffer_stream() override {
  }

  bool open(const void* p, uint size) {
    CRNLIB_ASSERT(p);

    close();

    if ((!p) || (!size))
      return false;

    m_opened = true;
    m_pBuf = (uint8*)(p);
    m_size = size;
    m_ofs = 0;
    m_attribs = cDataStreamSeekable | cDataStreamReadable;
    return true;
  }

  bool open(void* p, uint size) {
    CRNLIB_ASSERT(p);

    close();

    if ((!p) || (!size))
      return false;

    m_opened = true;
    m_pBuf = static_cast<uint8*>(p);
    m_size = size;
    m_ofs = 0;
    m_attribs = cDataStreamSeekable | cDataStreamWritable | cDataStreamReadable;
    return true;
  }

  bool close() override {
    if (m_opened) {
      m_opened = false;
      m_pBuf = nullptr;
      m_size = 0;
      m_ofs = 0;
      return true;
    }

    return false;
  }

  const void* get_buf() const { return m_pBuf; }
  void* get_buf() { return m_pBuf; }

  const void* get_ptr() const override { return m_pBuf; }

  uint read(void* pBuf, uint len) override {
    CRNLIB_ASSERT(pBuf && (len <= 0x7FFFFFFF));

    if ((!m_opened) || (!is_readable()) || (!len))
      return 0;

    CRNLIB_ASSERT(m_ofs <= m_size);

    uint bytes_left = m_size - m_ofs;

    len = math::minimum<uint>(len, bytes_left);

    if (len)
      memcpy(pBuf, &m_pBuf[m_ofs], len);

    m_ofs += len;

    return len;
  }

  uint write(const void* pBuf, uint len) override {
    CRNLIB_ASSERT(pBuf && (len <= 0x7FFFFFFF));

    if ((!m_opened) || (!is_writable()) || (!len))
      return 0;

    CRNLIB_ASSERT(m_ofs <= m_size);

    uint bytes_left = m_size - m_ofs;

    len = math::minimum<uint>(len, bytes_left);

    if (len)
      memcpy(&m_pBuf[m_ofs], pBuf, len);

    m_ofs += len;

    return len;
  }

  bool flush() override {
    if (!m_opened)
      return false;

    return true;
  }

  uint64 get_size() override {
    if (!m_opened)
      return 0;

    return m_size;
  }

  uint64 get_remaining() override {
    if (!m_opened)
      return 0;

    CRNLIB_ASSERT(m_ofs <= m_size);

    return m_size - m_ofs;
  }

  uint64 get_ofs() override {
    if (!m_opened)
      return 0;

    return m_ofs;
  }

  bool seek(int64 ofs, bool relative) override {
    if ((!m_opened) || (!is_seekable()))
      return false;

    int64 new_ofs = relative ? (m_ofs + ofs) : ofs;

    if (new_ofs < 0)
      return false;
    else if (new_ofs > m_size)
      return false;

    m_ofs = static_cast<uint>(new_ofs);

    post_seek();

    return true;
  }

 private:
  uint8* m_pBuf;
  uint m_size;
  uint m_ofs;
};

}  // namespace crnlib
