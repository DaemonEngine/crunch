#! /usr/bin/env python3

import hashlib
import os
import subprocess
import sys
from collections import OrderedDict

try:
    from colorama import Fore, Style
except ModuleNotFoundError:
    class Fore: CYAN = MAGENTA = GREEN = YELLOW = RED = ""
    class Style: RESET_ALL = ""

build_dir = os.getenv("CRUNCH_BUILD_DIR", "build")
executable_extension = os.getenv("CRUNCH_EXE_EXTENSION", "")
executable_runner = os.getenv("CRUNCH_EXE_RUNNER")
simple_test = os.getenv("CRUNCH_SIMPLE_TEST")
check_list = os.getenv("CRUNCH_CHECK_LIST", "files clones").split(" ")

database_path = "test/checksums.tsv"

file_knowledge = OrderedDict()
clone_knowledge = OrderedDict()

def print_status(message):
    print("{}{}{}".format(Fore.CYAN, message, Style.RESET_ALL), file=sys.stderr)

def print_notice(message):
    print("{}{}{}".format(Fore.MAGENTA, message, Style.RESET_ALL), file=sys.stderr)

def print_success(message):
    print("{}{}{}".format(Fore.GREEN, message, Style.RESET_ALL), file=sys.stderr)

def print_warning(message):
    print("{}Warning: {}{}".format(Fore.YELLOW, message, Style.RESET_ALL), file=sys.stderr)

def print_error(message):
    print("{}Error: {}{}".format(Fore.RED, message, Style.RESET_ALL), file=sys.stderr)
    exit(1)

def print_command_run(command_list):
    print_status("Running command: {}".format(" ".join(command_list)))

def print_command_success(command_list):
    print_success("Command succeeded: {}".format(" ".join(command_list)))

def convert_path(path):
    if path.startswith("build/"):
        path = build_dir + path[len("build"):]

    return path.replace("/", os.path.sep)

def get_file_sum(file_path):
    return hashlib.blake2b(open(file_path, "rb").read()).hexdigest()

def run(command_list):
    if executable_runner:
        command_list = executable_runner.split(" ") + command_list

    print_command_run(command_list)
    returncode = subprocess.run(command_list).returncode

    if returncode:
        print_error("Command failed: {}".format(" ".join(command_list)))
        exit(returncode)

    print_command_success(command_list)

def mkdir(path):
    path = convert_path(path)
    command_list = ["mkdir", path]
    print_command_run(command_list)
    os.makedirs(path, exist_ok=True)
    print_command_success(command_list)

def get_build_dir():
    windows_build_dir = os.path.join(build_dir, "Release")

    if os.path.exists(windows_build_dir):
        return windows_build_dir

    return build_dir

def get_executable_path(executable_name):
    executable_name += executable_extension
    build_dir = get_build_dir()

    return os.path.join(build_dir, executable_name)

def add_clone(clone, file_path):
    if not clone:
        return

    if clone not in clone_knowledge.keys():
        clone_knowledge[clone] = {}
        clone_knowledge[clone]["files"] = OrderedDict()


    clone_knowledge[clone]["files"][file_path] = False

def crunch(input_path, output_path, clone=None, options=[]):
    executable_path = get_executable_path("crunch")
    command_list = [executable_path] + options

    if input_path:
        converted_input_path = convert_path(input_path)
        command_list += ["-noTitle", "-helperThreads", "3", "-nostats", "-noprogress", "-file", converted_input_path]

    if output_path:
        converted_output_path = convert_path(output_path)
        command_list += ["-out", converted_output_path]
        file_knowledge[output_path] = {"converted_path": converted_output_path}
        add_clone(clone, output_path)

    run(command_list)

def example(num, input_path, output_path, clone=None, options=[]):
    executable_path = get_executable_path("example" + str(num))
    command_list = [executable_path]

    if (num == 1):
        command_list += [options[0]]
        options = options[1:]

    if input_path:
        converted_input_path = convert_path(input_path)
        command_list += [converted_input_path]

    command_list += options

    if output_path:
        converted_output_path = convert_path(output_path)
        command_list += ["-out", converted_output_path]
        file_knowledge[output_path] = {"converted_path": converted_output_path}
        add_clone(clone, output_path)

    run(command_list)

def sum_files():
    for file_path in file_knowledge.keys():
        print_status("Summing file {}".format(file_path))
        file_sum = get_file_sum(file_knowledge[file_path]["converted_path"])
        file_knowledge[file_path]["file_sum"] = file_sum
        print_notice("File {} has checksum {}".format(file_path, file_sum))

def record_sums():
    database_content = ""

    for file_path in file_knowledge.keys():
        database_content += "{}\t{}\n".format(file_path, file_knowledge[file_path]["file_sum"])

    database_file = open(database_path, "w")
    database_file.write(database_content)
    database_file.close()

    print_success("All test results recorded")

def verify_clones(verification):
    all_verified = True

    if verification:
        for file_clone in clone_knowledge.keys():
            for file_path in clone_knowledge[file_clone]["files"].keys():
                file_sum = file_knowledge[file_path]["file_sum"]

                if "known_sum" in clone_knowledge[file_clone].keys():
                    known_sum = clone_knowledge[file_clone]["known_sum"]
                    verified = file_sum == known_sum
                    clone_knowledge[file_clone]["files"][file_path] = verified

                    if verified:
                        print_success("Clone {}'s checksum {} matches known one".format(file_path, known_sum))
                    else:
                        print_warning("Clone {}'s checksum {} doesn't match known one {}".format(file_path, file_sum, known_sum))
                        all_verified = False

                else:
                    clone_knowledge[file_clone]["known_sum"] = file_sum

    return all_verified

def verify_files(verification):
    all_verified = True

    if verification:
        database_file = open(database_path, "r")

        for line in database_file.readlines():
            file_path, known_sum = line.split("\t")
            file_knowledge[file_path]["known_sum"] = known_sum.split("\n")[0]

        database_file.close()

        for file_path in file_knowledge.keys():
            print_status("Checking file {}".format(file_path))
            file_sum = file_knowledge[file_path]["file_sum"]
            known_sum = file_knowledge[file_path]["known_sum"]
            verified = file_sum == known_sum
            file_knowledge[file_path]["verified"] = verified

            if verified:
                print_success("File {}'s checksum {} matches known one".format(file_path, known_sum))
            else:
                print_warning("File {}'s checksum {} doesn't match known one {}".format(file_path, file_sum, known_sum))
                all_verified = False

    return all_verified

def print_clones_results(verification):
    if verification:
        print("Clones verification results:")
    else:
        print("Clones generation results:")

    for file_clone in clone_knowledge.keys():
        first = True
        for file_path in clone_knowledge[file_clone]["files"].keys():
            if first:
                verified_string = "---"
                first = False
            elif verification:
                verified = clone_knowledge[file_clone]["files"][file_path]
                verified_string = ["No", "Yes"][verified]
            else:
                verified_string = "???"

            short_sum = file_knowledge[file_path]["file_sum"][0:10]
            print("{:<3} {} {} {}".format(verified_string, short_sum, file_clone, file_path))

def print_files_results(verification):
    if verification:
        print("Files verification results:")
    else:
        print("Files generation results:")

    for file_path in file_knowledge.keys():
        if verification:
            verified = file_knowledge[file_path]["verified"]
            verified_string = ["No", "Yes"][verified]
        else:
            verified_string = "???"

        short_sum = file_knowledge[file_path]["file_sum"][0:10]
        print("{:<3} {} {}".format(verified_string, short_sum, file_path))

def print_end_results(clones_verification, clones_verified, files_verification, files_verified):
    if clones_verification:
        if clones_verified:
            print_success("All clones verified")
        else:
            print_warning("Some clones were not verified")

    if files_verification:
        if files_verified:
            print_success("All files verified")
        else:
            print_warning("Some files were not verified")

    if clones_verified and files_verified:
       print_success("All tests passed")
    else:
       print_error("Some tests failed")

crunch(None, None, options=["--help"])

if simple_test == "true":
    exit(0)

mkdir("build/test/png-to-all")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.tga", clone="tga")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.bmp", clone="bmp")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.png", clone="png")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.crn", clone="crn")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.dds", clone="dds")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.ktx", clone="ktx")
crunch("test/unvanquished_64.png", "build/test/png-to-all/unvanquished_64.jpg", clone="jpg")

mkdir("build/test/tga-to-all")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.tga", clone="tga")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.bmp", clone="bmp")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.png", clone="png")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.crn", clone="crn")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.dds", clone="dds")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.ktx", clone="ktx")
crunch("build/test/png-to-all/unvanquished_64.tga", "build/test/tga-to-all/unvanquished_64.jpg", clone="jpg")

mkdir("build/test/bmp-to-all")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.tga", clone="tga")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.bmp", clone="bmp")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.png", clone="png")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.crn", clone="crn")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.dds", clone="dds")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.ktx", clone="ktx")
crunch("build/test/png-to-all/unvanquished_64.bmp", "build/test/bmp-to-all/unvanquished_64.jpg", clone="jpg")

mkdir("build/test/crn-to-all")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.tga")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.bmp")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.png")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.crn")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.dds", clone="crn_dds")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.ktx")
crunch("build/test/png-to-all/unvanquished_64.crn", "build/test/crn-to-all/unvanquished_64.jpg")

mkdir("build/test/dds-to-all")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.tga")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.bmp")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.png")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.crn")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.dds", clone="dds")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.ktx")
crunch("build/test/png-to-all/unvanquished_64.dds", "build/test/dds-to-all/unvanquished_64.jpg")

mkdir("build/test/ktx-to-all")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.tga")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.bmp")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.png")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.crn")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.dds")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.ktx")
crunch("build/test/png-to-all/unvanquished_64.ktx", "build/test/ktx-to-all/unvanquished_64.jpg")

mkdir("build/test/jpg-to-all")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.tga")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.bmp")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.png")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.crn")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.dds")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.ktx")
crunch("build/test/png-to-all/unvanquished_64.jpg", "build/test/jpg-to-all/unvanquished_64.jpg")

mkdir("build/test/tga-to-png")
crunch("test/raw-bottom-left.tga", "build/test/tga-to-png/raw-bottom-left.png", clone="tga_png")
crunch("test/raw-bottom-right.tga", "build/test/tga-to-png/raw-bottom-right.png", clone="tga_png")
crunch("test/raw-top-left.tga", "build/test/tga-to-png/raw-top-left.png", clone="tga_png")
crunch("test/raw-top-right.tga", "build/test/tga-to-png/raw-top-right.png", clone="tga_png")
crunch("test/rle-bottom-left.tga", "build/test/tga-to-png/rle-bottom-left.png", clone="tga_png")
crunch("test/rle-bottom-right.tga", "build/test/tga-to-png/rle-bottom-right.png", clone="tga_png")
crunch("test/rle-top-left.tga", "build/test/tga-to-png/rle-top-left.png", clone="tga_png")
crunch("test/rle-top-right.tga", "build/test/tga-to-png/rle-top-right.png", clone="tga_png")

mkdir("build/test/tga-to-crn")
crunch("test/raw-bottom-left.tga", "build/test/tga-to-crn/raw-bottom-left.crn", clone="tga_crn")
crunch("test/raw-bottom-right.tga", "build/test/tga-to-crn/raw-bottom-right.crn", clone="tga_crn")
crunch("test/raw-top-left.tga", "build/test/tga-to-crn/raw-top-left.crn", clone="tga_crn")
crunch("test/raw-top-right.tga", "build/test/tga-to-crn/raw-top-right.crn", clone="tga_crn")
crunch("test/rle-bottom-left.tga", "build/test/tga-to-crn/rle-bottom-left.crn", clone="tga_crn")
crunch("test/rle-bottom-right.tga", "build/test/tga-to-crn/rle-bottom-right.crn", clone="tga_crn")
crunch("test/rle-top-left.tga", "build/test/tga-to-crn/rle-top-left.crn", clone="tga_crn")
crunch("test/rle-top-right.tga", "build/test/tga-to-crn/rle-top-right.crn", clone="tga_crn")

mkdir("build/test/png-to-png")
crunch("test/test-colormap1-alpha1.png", "build/test/png-to-png/test-colormap1-alpha1.png")
crunch("test/test-colormap2-alpha1.png", "build/test/png-to-png/test-colormap2-alpha1.png")
crunch("test/test-colormap4-alpha1.png", "build/test/png-to-png/test-colormap4-alpha1.png")
crunch("test/test-colormap8-alpha1.png", "build/test/png-to-png/test-colormap8-alpha1.png")
crunch("test/test-grayscale1-alpha1.png", "build/test/png-to-png/test-grayscale1-alpha1.png")
crunch("test/test-grayscale1-alpha8.png", "build/test/png-to-png/test-grayscale1-alpha8.png")
crunch("test/test-grayscale8-alpha1.png", "build/test/png-to-png/test-grayscale8-alpha1.png")
crunch("test/test-rgb8-alpha8.png", "build/test/png-to-png/test-rgb8-alpha8.png")

mkdir("build/test/png-to-crn")
crunch("test/test-colormap1-alpha1.png", "build/test/png-to-crn/test-colormap1-alpha1.crn")
crunch("test/test-colormap2-alpha1.png", "build/test/png-to-crn/test-colormap2-alpha1.crn")
crunch("test/test-colormap4-alpha1.png", "build/test/png-to-crn/test-colormap4-alpha1.crn")
crunch("test/test-colormap8-alpha1.png", "build/test/png-to-crn/test-colormap8-alpha1.crn")
crunch("test/test-grayscale1-alpha1.png", "build/test/png-to-crn/test-grayscale1-alpha1.crn")
crunch("test/test-grayscale1-alpha8.png", "build/test/png-to-crn/test-grayscale1-alpha8.crn")
crunch("test/test-grayscale8-alpha1.png", "build/test/png-to-crn/test-grayscale8-alpha1.crn")
crunch("test/test-rgb8-alpha8.png", "build/test/png-to-crn/test-rgb8-alpha8.crn")

mkdir("build/test/bmp-to-crn")
crunch("test/sample-default.bmp", "build/test/bmp-to-crn/sample-default.crn", "bmp_crn")
crunch("test/sample-vertical-flip.bmp", "build/test/bmp-to-crn/sample-vertical-flip.crn", "bmp_crn")

mkdir("build/test/jpg-to-crn")
crunch("test/black.jpg", "build/test/jpg-to-crn/black.crn")

mkdir("build/test/example1-dds")
example(1, "test/unvanquished_64.png", None, options=["i"])
example(1, "test/unvanquished_64.png", "build/test/example1-dds/unvanquished_64.dds", clone="dds", options=["c"])

mkdir("build/test/example1-crn")
example(1, "test/unvanquished_64.png", "build/test/example1-crn/unvanquished_64.crn", clone="crn", options=["c", "-crn"])
example(1, "build/test/example1-crn/unvanquished_64.crn", "build/test/example1-crn/unvanquished_64.dds", clone="crn_dds", options=["d"])

mkdir("build/test/example2-dds")
example(2, "build/test/example1-crn/unvanquished_64.crn", "build/test/example2-dds/unvanquished_64.dds", clone="crn_dds")

mkdir("build/test/example3-dds")
example(3, "test/unvanquished_64.png", "build/test/example3-dds/unvanquished_64.dds")

print_success("All tests executed")

sum_files()

all_verified = True
clones_verification = "clones" in check_list
files_verification = "files" in check_list

recording = sys.argv[1:] == ["--record"]

if recording:
    clones_verification = False
    files_verification = False
    record_sums()

clones_verified = verify_clones(clones_verification)

files_verified = verify_files(files_verification)

print_clones_results(clones_verification)

print_files_results(files_verification)

print_end_results(clones_verification, clones_verified, files_verification, files_verified)
