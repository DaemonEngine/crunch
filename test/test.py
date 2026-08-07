#! /usr/bin/env python3

import hashlib
import os
import subprocess
import sys
from collections import OrderedDict
from itertools import chain

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
    if executable_runner and executable_runner.endswith("wine"):
        wineserver = f"{executable_runner}server"
        subprocess.run([wineserver, "-k"], check=False)

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

def add_clone(clone_name, file_path):
    if not clone_name:
        return

    if clone_name not in clone_knowledge.keys():
        clone_knowledge[clone_name] = {}
        clone_knowledge[clone_name]["files"] = OrderedDict()

    clone_knowledge[clone_name]["files"][file_path] = False

def crunch(input_path, output_path, clone_name, options=[]):
    executable_path = get_executable_path("crunch")
    command_list = [executable_path] + options

    if input_path:
        converted_input_path = convert_path(input_path)
        command_list += ["-noTitle", "-helperThreads", "3", "-nostats", "-noprogress", "-noNormalDetection", "-file", converted_input_path]

    if output_path:
        converted_output_path = convert_path(output_path)
        command_list += ["-out", converted_output_path]
        file_knowledge[output_path] = {"converted_path": converted_output_path}
        add_clone(clone_name, output_path)

    run(command_list)

def example(num, input_path, output_path, clone_name, options=[]):
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
        add_clone(clone_name, output_path)

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
    clones_verified = 0
    clones_failed = 0

    if verification:
        for file_clone in clone_knowledge.keys():
            for file_path in clone_knowledge[file_clone]["files"].keys():
                if file_path not in file_knowledge.keys():
                    continue

                file_sum = file_knowledge[file_path]["file_sum"]

                if "known_sum" in clone_knowledge[file_clone].keys():
                    known_sum = clone_knowledge[file_clone]["known_sum"]
                    verified = file_sum == known_sum
                    clone_knowledge[file_clone]["files"][file_path] = verified

                    if verified:
                        print_success("Clone {}'s checksum {} matches known one".format(file_path, known_sum))
                        clones_verified += 1

                        # Count the first clone as verified once the second one is found and is verified.
                        if len(clone_knowledge[file_clone]["files"].keys()) == 1:
                            clones_verified += 1
                    else:
                        print_warning("Clone {}'s checksum {} doesn't match known one {}".format(file_path, file_sum, known_sum))
                        clones_failed += 1

                        # Count the first clone as failed once the second one is found and is failed.
                        if len(clone_knowledge[file_clone]["files"].keys()) == 1:
                            clones_verified += 1

                else:
                    clone_knowledge[file_clone]["known_sum"] = file_sum

                    # Do not count the first clone as verified or failed until a second clone is seen and verified.

    return clones_verified, clones_failed

def verify_files(verification):
    files_verified = 0
    files_failed = 0

    if verification:
        database_file = open(database_path, "r")

        for line in database_file.readlines():
            file_path, known_sum = line.split("\t")

            file_knowledge[file_path]["known_sum"] = known_sum.split("\n")[0]

        database_file.close()

        for file_path in file_knowledge.keys():
            print_status("Checking file {}".format(file_path))
            file_sum = file_knowledge[file_path]["file_sum"]

            if "known_sum" not in file_knowledge[file_path].keys():
                print_warning(f"Missing recorded sum for {file_path}")
                files_failed += 1
                continue

            known_sum = file_knowledge[file_path]["known_sum"]
            verified = file_sum == known_sum
            file_knowledge[file_path]["verified"] = verified

            if verified:
                print_success("File {}'s checksum {} matches known one".format(file_path, known_sum))
                files_verified += 1
            else:
                print_warning("File {}'s checksum {} doesn't match known one {}".format(file_path, file_sum, known_sum))
                files_verified += 1

    return files_verified, files_failed

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
            if "verified" not in file_knowledge[file_path].keys():
                print_warning(f"Missing verified status for {file_path}")
                continue

            verified = file_knowledge[file_path]["verified"]
            verified_string = ["No", "Yes"][verified]
        else:
            verified_string = "???"

        short_sum = file_knowledge[file_path]["file_sum"][0:10]
        print("{:<3} {} {}".format(verified_string, short_sum, file_path))

def print_end_results(clones_verification, clones_verified, clones_failed, files_verification, files_verified, files_failed):
    if clones_verification:
        clones_total = clones_verified + clones_failed
        if not clones_failed:
            print_success(f"All clones verified (total: {clones_total})")
        else:
            print_warning(f"Some clones were not verified (verified: {clones_verified}, failed: {clones_failed}, total: {clones_total})")

    if files_verification:
        files_total = files_verified + files_failed
        if not files_failed:
            print_success(f"All files verified (total: {files_total})")
        else:
            print_warning(f"Some files were not verified (verified: {files_verified}, failed: {files_failed}, total: {files_total})")

    tests_verified = clones_verified + files_verified
    tests_failed = clones_failed + files_failed
    tests_total = tests_verified + tests_failed
    if not tests_failed:
       print_success(f"All tests passed (total: {tests_total})")
    else:
       print_error(f"Some tests failed (verified: {tests_verified}, failed: {tests_failed}, total: {tests_total})")

crunch(None, None, None, options=["--help"])

def merge_list(*lists):
    return list(dict.fromkeys(chain.from_iterable(lists)))

def start_from(items, value):
    i = items.index(value)
    return items[i:] + items[:i]

if simple_test == "true":
    exit(0)

lossless_format_list = [
    "tga",
    "bmp",
    "png",
]

lossy_format_list = [
    "crn",
    "dds",
    "ktx",
    "jpg",
]

dxt_format_list = [
    "crn",
    "dds",
    "ktx",
]

transparent_format_list = [
    "tga",
    "bmp",
    "png",
    "crn",
    "dds",
    "ktx",
]

opaque_format_list = [
    "jpg",
]

all_format_list = merge_list(
    lossless_format_list,
    dxt_format_list,
    transparent_format_list,
    opaque_format_list,
    lossy_format_list,
)

for in_format in start_from(all_format_list, "png"):
    if in_format == "png":
        in_dir = "test"
    else:
        in_dir = "build/test/crunch-icon-png-to-all"

    out_dir = f"build/test/crunch-icon-{in_format}-to-all"

    mkdir(out_dir)

    for out_format in all_format_list:
        sample_name = "sample-icon-unvanquished-64x64"

        in_path = f"{in_dir}/{sample_name}.{in_format}"

        out_path = f"{out_dir}/{sample_name}.{out_format}"

        if in_format in lossless_format_list:
            clone_name = f"icon-png-to-{out_format}"
        elif in_format == out_format and out_format in ["dds", "ktx"]:
            clone_name = f"icon-png-to-{out_format}"
        elif in_format == "crn" and out_format == "dds":
            clone_name = f"icon-{in_format}-to-{out_format}"
        else:
            clone_name = None

        crunch(in_path, out_path, clone_name)

collection_dict_list = [
    {
        "name": "orientation",
        "format": "tga",
        "clone": True,
        "samples": [
            "sample-flat-bottom-left",
            "sample-flat-bottom-right",
            "sample-flat-top-left",
            "sample-flat-top-right",
            "sample-rle-bottom-left",
            "sample-rle-bottom-right",
            "sample-rle-top-left",
            "sample-rle-top-right",
        ],
    },
    {
        "name": "orientation",
        "format": "bmp",
        "clone": True,
        "samples": [
            "sample-default",
            "sample-vertical-flip",
        ],
    },
    {
        "name": "transparency",
        "format": "png",
        "clone": False,
        "samples": [
            "sample-colormap1-alpha1",
            "sample-colormap2-alpha1",
            "sample-colormap4-alpha1",
            "sample-colormap8-alpha1",
            "sample-grayscale1-alpha1",
            "sample-grayscale1-alpha8",
            "sample-grayscale8-alpha1",
            "sample-rgb8-alpha8",
        ],
    },
    {
        "name": "format",
        "clone": False,
        "format": "jpg",
        "samples": [
            "sample-black-64x64",
            "sample-grayscale-sampling1x1",
            "sample-grayscale-sampling2x2",
        ],
    },
]

for collection in collection_dict_list:
    collection_name = collection["name"]
    in_format = collection["format"]
    is_clone = collection["clone"]
    sample_name_list = collection["samples"]

    out_dir = f"build/test/crunch-{collection_name}-{in_format}-to-all"

    mkdir(out_dir)

    for sample_name in sample_name_list:
        for out_format in all_format_list:
            in_path = f"test/{sample_name}.{in_format}"

            out_path = f"{out_dir}/{sample_name}.{out_format}"

            if is_clone:
                clone_name = f"{collection_name}-{in_format}-to-{out_format}"
            else:
                clone_name = None

            crunch(in_path, out_path, clone_name)

for encoding in [
    "flat",
    "rle",
]:
    for alpha_type in [
        "noalpha",
        "alpha8",
        "other8",
    ]:
        for alpha_name in [
            "opaque",
            "transparent",
        ]:
            for color_type in [
                "grayscale8",
                "rgb8",
            ]:
                for color_name, base_width in [
                    ("white", 1),
                    ("red", 1),
                    ("color", 2),
                ]:
                    if encoding == "rle":
                        if color_name == "color":
                            width_list = [base_width, base_width * 4]
                        else:
                            width_list = [base_width * 2]
                    else:
                        width_list = [base_width]

                    for width in width_list:
                        for out_format in all_format_list:
                            if out_format in lossy_format_list and color_name == "color":
                                # Lossy or block-compressed formats require a larger color test image to
                                # preserve clearly distinguishable red/green/blue/white regions.
                                # Smaller images can introduce unavoidable artifacts from JPEG chroma
                                # subsampling or block-based texture compression (CRN/DDS/KTX), making
                                # visual validation unreliable.
                                #
                                # A minimum image width of 8 gives each color quadrant at least 4×4 pixels:
                                #  ______________
                                # |      |       |
                                # | red  | green |
                                # |      |       |
                                # |‒‒‒‒‒‒‒‒‒‒‒‒‒‒|
                                # |      |       |
                                # | blue | white |
                                # |      |       |
                                #  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                                if width < 8:
                                    continue

                            if color_type == "grayscale8" and not color_name == "white":
                                continue

                            if alpha_type == "noalpha" and alpha_name == "transparent":
                                continue

                            base_name = f"sample-storage-{encoding}-{color_type}-{alpha_type}-{color_name}-{alpha_name}-{width}x{width}"

                            in_format = 'tga'
                            in_path = f"test/{base_name}.{in_format}"

                            out_alpha_name = alpha_name

                            if out_format in opaque_format_list:
                                out_alpha_name = "opaque"

                            out_dir = f"build/test/{in_format}-to-all-{out_alpha_name}"
                            out_path = f"{out_dir}/{base_name}.{out_format}"

                            clone_name = f"{color_name}_{out_alpha_name}_{width}_{in_format}_{out_format}"

                            mkdir(out_dir)
                            crunch(in_path, out_path, clone_name)

example(1, "test/sample-icon-unvanquished-64x64.png", None, None, options=["i"])

mkdir("build/test/example1-icon-png-to-dds")
example(1, "test/sample-icon-unvanquished-64x64.png", "build/test/example1-icon-png-to-dds/sample-icon-unvanquished-64x64.dds", "icon-png-to-dds", options=["c"])

mkdir("build/test/example1-icon-png-to-crn")
example(1, "test/sample-icon-unvanquished-64x64.png", "build/test/example1-icon-png-to-crn/sample-icon-unvanquished-64x64.crn", "icon-png-to-crn", options=["c", "-crn"])

mkdir("build/test/example1-icon-crn-to-dds")
example(1, "build/test/example1-icon-png-to-crn/sample-icon-unvanquished-64x64.crn", "build/test/example1-icon-crn-to-dds/sample-icon-unvanquished-64x64.dds", "icon-crn-to-dds", options=["d"])

mkdir("build/test/example2-icon-crn-to-dds")
example(2, "build/test/example1-icon-png-to-crn/sample-icon-unvanquished-64x64.crn", "build/test/example2-icon-crn-to-dds/sample-icon-unvanquished-64x64.dds", "icon-crn-to-dds")

mkdir("build/test/example3-icon-png-to-dds")
example(3, "test/sample-icon-unvanquished-64x64.png", "build/test/example3-icon-png-to-dds/sample-icon-unvanquished-64x64.dds", None)

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

clones_verified, clones_failed = verify_clones(clones_verification)

files_verified, files_failed = verify_files(files_verification)

print_clones_results(clones_verification)

print_files_results(files_verification)

print_end_results(clones_verification, clones_verified, clones_failed, files_verification, files_verified, files_failed)
