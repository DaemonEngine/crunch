include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc
)

# Defines the source code for the library
set(CRNLIB_SRCS
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_arealist.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_arealist.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_assert.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_assert.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_buffer_stream.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_cfile_stream.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_checksum.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_checksum.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_clusterizer.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_color.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_colorized_console.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_colorized_console.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_command_line_params.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_command_line_params.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_comp.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_comp.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_console.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_console.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_core.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_core.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_data_stream.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_data_stream.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_data_stream_serializer.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dds_comp.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dds_comp.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_decomp.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt1.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt1.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt5a.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt5a.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_endpoint_refiner.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_endpoint_refiner.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_fast.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_fast.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_hc.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_hc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_hc_common.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_hc_common.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_image.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dxt_image.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dynamic_stream.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dynamic_string.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_dynamic_string.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_etc.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_etc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_file_utils.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_file_utils.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_find_files.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_find_files.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_hash.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_hash.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_hash_map.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_hash_map.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_helpers.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_huffman_codes.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_huffman_codes.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_image.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_image_utils.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_image_utils.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_intersect.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_jpgd.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_jpgd.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_jpge.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_jpge.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ktx_texture.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ktx_texture.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_lzma_codec.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_lzma_codec.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_math.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_math.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_matrix.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_mem.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_mem.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_miniz.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_miniz.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_mipmapped_texture.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_mipmapped_texture.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_packed_uint.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_pixel_format.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_pixel_format.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_platform.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_platform.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_prefix_coding.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_prefix_coding.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_qdxt1.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_qdxt1.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_qdxt5.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_qdxt5.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_rand.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_rand.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ray.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_rect.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_resample_filters.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_resample_filters.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_resampler.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_resampler.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_rg_etc1.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_rg_etc1.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ryg_dxt.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ryg_dxt.hpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_ryg_types.hpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_sparse_array.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_sparse_bit_array.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_sparse_bit_array.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_stb_image.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_strutils.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_strutils.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_symbol_codec.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_symbol_codec.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_comp.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_comp.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_conversion.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_conversion.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_file_types.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_texture_file_types.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_threaded_clusterizer.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_threaded_resampler.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_threaded_resampler.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading_null.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_timer.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_timer.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_traits.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_tree_clusterizer.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_types.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_utils.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_utils.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_value.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_value.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_vec.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_vec_interval.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_vector.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_vector.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_vector2d.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crn_winhdr.h
  ${CMAKE_CURRENT_SOURCE_DIR}/crnlib.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zBuf.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zBuf.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zBuf2.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zCrc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zFile.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zFile.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zStream.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_7zVersion.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Alloc.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Alloc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Bcj2.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Bcj2.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Bra.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Bra.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Bra86.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_BraIA64.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_CpuArch.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzFind.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzFind.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzHash.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaDec.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaDec.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaEnc.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaEnc.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaLib.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzmaLib.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_MyVersion.h
  ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Types.h
  ${CMAKE_CURRENT_SOURCE_DIR}/stb_image.h
  ${CMAKE_CURRENT_SOURCE_DIR}/stb_image_write.h
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc/crn_decomp.h
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc/crnlib.h
  ${CMAKE_CURRENT_SOURCE_DIR}/../inc/dds_defs.h
)

if(WIN32)
  set(CRNLIB_THREAD_SRCS
    ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzFindMt.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/lzma_LzFindMt.h
    ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Threads.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/lzma_Threads.h
    ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading_win32.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading_win32.h
  )
else()
  set(CRNLIB_THREAD_SRCS
    ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading_pthreads.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/crn_threading_pthreads.h
  )
endif()

set(CRUNCH_OBJECT_NAME ${CRUNCH_LIBRARY_NAME}-obj)
add_library(${CRUNCH_OBJECT_NAME} OBJECT ${CRNLIB_SRCS} ${CRNLIB_THREAD_SRCS})
set_property(TARGET ${CRUNCH_OBJECT_NAME} PROPERTY POSITION_INDEPENDENT_CODE 1)

if(BUILD_SHARED_LIBS)
  set(CRUNCH_DEFAULT_LIBRARY_TYPE SHARED)
  set(CRUNCH_OTHER_LIBRARY_TYPE STATIC)
  set(CRUNCH_OTHER_LIBRARY_SUFFIX -static)
else()
  set(CRUNCH_DEFAULT_LIBRARY_TYPE STATIC)
  set(CRUNCH_OTHER_LIBRARY_TYPE SHARED)
  set(CRUNCH_OTHER_LIBRARY_SUFFIX -shared)
endif()

add_library(${CRUNCH_LIBRARY_NAME} ${CRUNCH_DEFAULT_LIBRARY_TYPE} $<TARGET_OBJECTS:${CRUNCH_OBJECT_NAME}>)
set_property(TARGET ${CRUNCH_LIBRARY_NAME} PROPERTY POSITION_INDEPENDENT_CODE 1)

if (BUILD_SHARED_LIBS OR (BUILD_STATIC_LIBCRN AND INSTALL_STATIC_LIBCRN))
  install(TARGETS ${CRUNCH_LIBRARY_NAME} DESTINATION lib)
endif()

if ((BUILD_SHARED_LIBS AND BUILD_STATIC_LIBCRN) OR (NOT BUILD_SHARED_LIBS AND BUILD_SHARED_LIBCRN))
  set(CRUNCH_OTHER_LIBRARY_NAME ${CRUNCH_LIBRARY_NAME}${CRUNCH_OTHER_LIBRARY_SUFFIX})

  add_library(${CRUNCH_OTHER_LIBRARY_NAME} ${CRUNCH_OTHER_LIBRARY_TYPE} $<TARGET_OBJECTS:${CRUNCH_OBJECT_NAME}>)
  set_property(TARGET ${CRUNCH_OTHER_LIBRARY_NAME} PROPERTY POSITION_INDEPENDENT_CODE 1)

  if(NOT WIN32)
    set_target_properties(${CRUNCH_OTHER_LIBRARY_NAME} PROPERTIES OUTPUT_NAME ${CRUNCH_LIBRARY_NAME})
  endif()

  install(TARGETS ${CRUNCH_OTHER_LIBRARY_NAME} DESTINATION lib)
endif()
