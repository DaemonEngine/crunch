#! /usr/bin/env python3

import os
import subprocess
import sys

def print_command(command_list):
    print("running: " + " ".join(command_list), file=sys.stderr)

def convert_path(path):
    return path.replace("/", os.path.sep)

def run(command_list):
    print_command(command_list)
    returncode = subprocess.run(command_list).returncode
    if returncode:
        exit(returncode)

def mkdir(path):
    print_command(["mkdir", path])
    os.makedirs(path, exist_ok=True)

def crunch(input_path, output_path, options=[]):
    executable_extension = ["", ".exe"][sys.platform == 'win32']
    executable_name = "crunch" + executable_extension

    build_dir = "build"
    windows_build_dir = os.path.join(build_dir, "Release")
    if os.path.exists(windows_build_dir):
        build_dir = windows_build_dir

    executable_path = os.path.join(build_dir, executable_name)
    command_list = [executable_path] + options

    if input_path:
        input_path = convert_path(input_path)
        output_path = convert_path(output_path)
        command_list += ["-noTitle", "-file", input_path, "-out", output_path]

    run(command_list)

crunch(None, None, ["--help"])

mkdir("build/test/0")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.crn")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.dds")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.ktx")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.tga")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.bmp")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.png")
crunch("test/unvanquished_64.png", "build/test/0/unvanquished_64.jpg")

mkdir("build/test/1")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.crn")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.dds")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.ktx")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.tga")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.bmp")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.png")
crunch("build/test/0/unvanquished_64.crn", "build/test/1/unvanquished_64.jpg")

mkdir("build/test/2")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.crn")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.dds")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.ktx")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.tga")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.bmp")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.png")
crunch("build/test/0/unvanquished_64.dds", "build/test/2/unvanquished_64.jpg")

mkdir("build/test/3")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.crn")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.dds")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.ktx")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.tga")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.bmp")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.png")
crunch("build/test/0/unvanquished_64.ktx", "build/test/3/unvanquished_64.jpg")

mkdir("build/test/4")
crunch("test/raw-bottom-left.tga", "build/test/4/raw-bottom-left.crn")
crunch("test/raw-bottom-right.tga", "build/test/4/raw-bottom-right.crn")
crunch("test/raw-top-left.tga", "build/test/4/raw-top-left.crn")
crunch("test/raw-top-right.tga", "build/test/4/raw-top-right.crn")

mkdir("build/test/5")
crunch("test/test-colormap1-alpha1.png", "build/test/5/test-colormap1-alpha1.crn")
crunch("test/test-colormap2-alpha1.png", "build/test/5/test-colormap2-alpha1.crn")
crunch("test/test-colormap4-alpha1.png", "build/test/5/test-colormap4-alpha1.crn")
crunch("test/test-colormap8-alpha1.png", "build/test/5/test-colormap8-alpha1.crn")
crunch("test/test-grayscale1-alpha1.png", "build/test/5/test-grayscale1-alpha1.crn")
crunch("test/test-grayscale1-alpha8.png", "build/test/5/test-grayscale1-alpha8.crn")
crunch("test/test-grayscale8-alpha1.png", "build/test/5/test-grayscale8-alpha1.crn")
crunch("test/test-rgb8-alpha8.png", "build/test/5/test-rgb8-alpha8.crn")

mkdir("build/test/6")
crunch("test/sample-default.bmp", "build/test/6/sample-default.crn")
crunch("test/sample-vertical-flip.bmp", "build/test/6/sample-vertical-flip.crn")

mkdir("build/test/7")
crunch("test/black.jpg", "build/test/7/black.crn")
