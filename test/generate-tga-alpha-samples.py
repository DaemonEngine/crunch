#!/usr/bin/env python3

# Author:  Thomas DEBESSE <dev@illwieckz.net>
# License: CC0 1.0
#
# This source code is covered by the CC0 1.0 Universal (CC0 1.0)
# “Public Domain Dedication” license, as described on this page:
# - https://creativecommons.org/publicdomain/zero/1.0/legalcode

import struct


def writeRLE(data, pixels):
	"""
	Write TGA RLE packets.

	pixels: list of complete pixel byte strings.
	"""
	i = 0

	while i < len(pixels):
		# Check for a run of identical pixels.
		run_length = 1
		while (
			i + run_length < len(pixels)
			and pixels[i + run_length] == pixels[i]
			and run_length < 128
		):
			run_length += 1

		if run_length >= 2:
			# RLE packet: high bit set, count - 1
			data.append(0x80 | (run_length - 1))
			data.extend(pixels[i])
			i += run_length
		else:
			# Raw packet: high bit clear
			raw_start = i
			raw_length = 1

			while (
				raw_start + raw_length < len(pixels)
				and raw_length < 128
			):
				# Stop before a run.
				if (
					raw_start + raw_length + 1 < len(pixels)
					and pixels[raw_start + raw_length] ==
					pixels[raw_start + raw_length + 1]
				):
					break

				raw_length += 1

			data.append(raw_length - 1)

			for j in range(raw_start, raw_start + raw_length):
				data.extend(pixels[j])

			i += raw_length


def writeTGA(filename, width, height, pixels, pixel_depth, has_alpha, grayscale=False, rle=False):
	"""
	Write an uncompressed TGA.

	pixels: list of (r, g, b, a) tuples, top-left order.

	pixel_depth:
	  8  = grayscale
	  16 = grayscale + extra 8-bit component
	  24 = RGB8
	  32 = RGB8 + extra 8-bit component

	has_alpha:
	  True  = alpha attribute declared
	  False = no alpha attribute declared

	grayscale:
	  True  = TGA grayscale image type
	  False = true-color TGA
	"""
	if pixel_depth not in (8, 16, 24, 32):
		raise ValueError("invalid pixel depth")

	if grayscale:
		image_type = 11 if rle else 3
	else:
		image_type = 10 if rle else 2

	image_descriptor = 0x08 if has_alpha else 0x00

	header = struct.pack(
		"<BBBHHBHHHHBB",
		# id length
		0,
		# color map type
		0,
		image_type,
		# color map spec
		0, 0, 0,
		# x/y origin
		0, 0,
		width,
		height,
		pixel_depth,
		image_descriptor,
	)

	pixel_data = []

	# TGA default origin is bottom-left, so write rows reversed.
	for row in reversed(range(height)):
		for col in range(width):
			r, g, b, a = pixels[row * width + col]

			if grayscale:
				p = bytes((r,))
				if pixel_depth == 16:
					p += bytes((a,))
			else:
				p = bytes((b, g, r))
				if pixel_depth == 32:
					p += bytes((a,))

			pixel_data.append(p)

	data = bytearray()

	if rle:
		writeRLE(data, pixel_data)
	else:
		for p in pixel_data:
			data.extend(p)

	print(f"Generating: {filename}")

	with open(filename, "wb") as f:
		f.write(header)
		f.write(data)


def scaleImage(image, src_width, scale):
	pixels = []

	for y in range(src_width):
		for yy in range(scale):
			for x in range(src_width):
				for xx in range(scale):
					pixels.append(image[y * src_width + x])

	return pixels


def pixel(r, g, b, a=255):
	return (r, g, b, a)


# Grayscale white samples.
for encoding, width, has_rle in [
	("flat", 1, False),
	("rle", 2, True),
]:
	for alpha_type, has_alpha in [
		("alpha8", True),
		("other8", False),
	]:
		for alpha_name, alpha_value in [
			("opaque", 255),
			("transparent", 0),
		]:
			writeTGA(
				f"sample-storage-{encoding}-grayscale8-{alpha_type}-white-{alpha_name}-{width}x{width}.tga",
				width, width,
				[pixel(255, 255, 255, alpha_value)] * (width ** 2),
				16,
				has_alpha,
				True,
				has_rle,
			)

	writeTGA(
		f"sample-storage-{encoding}-grayscale8-noalpha-white-opaque-{width}x{width}.tga",
		width, width,
		[pixel(255, 255, 255)] * (width ** 2),
		8,
		False,
		True,
		has_rle,
	)

# White and red samples
colors = [
	("white", (255, 255, 255)),
	("red",   (255, 0, 0)),
]

for encoding, width, has_rle in [
	("flat", 1, False),
	("rle", 2, True),
]:
	for color_name, rgb in colors:
		for alpha_type, has_alpha in [
			("alpha8", True),
			("other8", False),
		]:
			for alpha_name, alpha_value in [
				("opaque", 255),
				("transparent", 0),
			]:
				writeTGA(
					f"sample-storage-{encoding}-rgb8-{alpha_type}-{color_name}-{alpha_name}-{width}x{width}.tga",
					width, width,
					[pixel(*rgb, alpha_value)] * (width ** 2),
					32,
					has_alpha,
					False,
					has_rle,
				)

		writeTGA(
			f"sample-storage-{encoding}-rgb8-noalpha-{color_name}-opaque-{width}x{width}.tga",
			width, width,
			[pixel(*rgb)] * (width ** 2),
			24,
			False,
			False,
			has_rle,
		)

# Color samples:
#  ______________
# |      |       |
# | red  | green |
# |      |       |
# |‒‒‒‒‒‒‒‒‒‒‒‒‒‒|
# |      |       |
# | blue | white |
# |      |       |
#  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾
rgba_image = [
	pixel(255, 0,   0),
	pixel(0,   255, 0),
	pixel(0,   0,   255),
	pixel(255, 255, 255),
]

for encoding, width, has_rle in [
	("flat", 2, False),
	("rle", 2, True),
	("rle", 8, True),
]:
	for alpha_name, alpha_value in [
		("opaque", 255),
		("transparent", 0),
	]:
		image = rgba_image.copy()

		r, g, b, _ = image[3]
		image[3] = pixel(r, g, b, alpha_value)

		pixels = scaleImage(image, 2, width // 2)

		for alpha_type, has_alpha in [
			("alpha8", True),
			("other8", False),
		]:
			writeTGA(
				f"sample-storage-{encoding}-rgb8-{alpha_type}-color-{alpha_name}-{width}x{width}.tga",
				width,
				width,
				pixels,
				32,
				has_alpha,
				False,
				has_rle,
			)

	# RGB-only variant
	pixels = scaleImage(rgba_image, 2, width // 2)

	writeTGA(
		f"sample-storage-{encoding}-rgb8-noalpha-color-opaque-{width}x{width}.tga",
		width,
		width,
		pixels,
		24,
		False,
		False,
		has_rle,
	)
