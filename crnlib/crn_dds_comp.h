// File: crn_comp.h
// See Copyright Notice and license at the end of inc/crnlib.h
#pragma once
#include "crn_comp.h"
#include "crn_mipmapped_texture.h"
#include "crn_texture_comp.h"

namespace crnlib {
class dds_comp : public itexture_comp {
  CRNLIB_NO_COPY_OR_ASSIGNMENT_OP(dds_comp);

 public:
  dds_comp();
  ~dds_comp() override;

  const char* get_ext() const override { return "DDS"; }

  bool compress_init(const crn_comp_params& params) override;
  bool compress_pass(const crn_comp_params& params, float* pEffective_bitrate) override;
  void compress_deinit() override;

  const crnlib::vector<uint8>& get_comp_data() const override { return m_comp_data; }
  crnlib::vector<uint8>& get_comp_data() override { return m_comp_data; }

 private:
  mipmapped_texture m_src_tex;
  mipmapped_texture m_packed_tex;

  crnlib::vector<uint8> m_comp_data;

  const crn_comp_params* m_pParams;

  pixel_format m_pixel_fmt;
  dxt_image::pack_params m_pack_params;

  task_pool m_task_pool;
  qdxt1_params m_q1_params;
  qdxt5_params m_q5_params;
  mipmapped_texture::qdxt_state* m_pQDXT_state;

  void clear();
  bool create_dds_tex(mipmapped_texture& dds_tex);
  bool convert_to_dxt(const crn_comp_params& params);
};

}  // namespace crnlib
