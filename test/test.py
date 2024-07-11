#! /usr/bin/env python3

import os
import subprocess
import sys

build_dir = os.getenv("CRUNCH_BUILD_DIR", "build")
executable_extension = os.getenv("CRUNCH_EXE_EXTENSION", "")
executable_runner = os.getenv("CRUNCH_EXE_RUNNER")

def print_command(command_list):
    print("running: " + " ".join(command_list), file=sys.stderr)

def convert_path(path):
    if path.startswith("build/"):
        path = build_dir + path[len("build"):]
    return path.replace("/", os.path.sep)

def run(command_list):
    if executable_runner:
        command_list = executable_runner.split(" ") + command_list
    print_command(command_list)
    returncode = subprocess.run(command_list).returncode
    if returncode:
        exit(returncode)

def mkdir(path):
    path = convert_path(path)
    print_command(["mkdir", path])
    os.makedirs(path, exist_ok=True)

def get_build_dir():
    windows_build_dir = os.path.join(build_dir, "Release")
    if os.path.exists(windows_build_dir):
        return windows_build_dir
    return build_dir

def get_executable_path(executable_name):
    executable_name += executable_extension
    build_dir = get_build_dir()
    return os.path.join(build_dir, executable_name)

def crunch(input_path, output_path, options=[]):
    executable_path = get_executable_path("crunch")
    command_list = [executable_path] + options

    if input_path:
        input_path = convert_path(input_path)
        output_path = convert_path(output_path)
        command_list += ["-noTitle", "-file", input_path, "-out", output_path]

    run(command_list)

def example(num, input_path, output_path, options=[]):
    executable_path = get_executable_path("example" + str(num))
    command_list = [executable_path] 

    if (num == 1):
        command_list += [options[0]]
        options = options[1:]

    if input_path:
        input_path = convert_path(input_path)
        command_list += [input_path]

    command_list += options

    if output_path:
        output_path = convert_path(output_path)
        command_list += ["-out", output_path]

    run(command_list)

crunch(None, None, ["--help"])

if "CRUNCH_SIMPLE_TEST" in os.environ.keys():
    exit(0)

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
crunch("test/rle-bottom-left.tga", "build/test/4/rle-bottom-left.crn")
crunch("test/rle-bottom-right.tga", "build/test/4/rle-bottom-right.crn")
crunch("test/rle-top-left.tga", "build/test/4/rle-top-left.crn")
crunch("test/rle-top-right.tga", "build/test/4/rle-top-right.crn")

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

mkdir("build/test/8")
example(1, "test/unvanquished_64.png", None, ["i"])
example(1, "test/unvanquished_64.png", "build/test/8/unvanquished_64.dds", ["c"])

mkdir("build/test/9")
example(1, "test/unvanquished_64.png", "build/test/9/unvanquished_64.crn", ["c", "-crn"])
example(1, "build/test/9/unvanquished_64.crn", "build/test/9/unvanquished_64.dds", ["d"])

mkdir("build/test/10")
example(2, "build/test/9/unvanquished_64.crn", "build/test/10/unvanquished_64.dds")

mkdir("build/test/11")
example(3, "test/unvanquished_64.png", "build/test/11/unvanquished_64.dds")
