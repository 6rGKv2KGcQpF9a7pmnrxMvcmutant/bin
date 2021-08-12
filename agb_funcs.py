#### utility function used in ./auto-gen-bookmarks.py

import json
from os import remove
import subprocess
from string import punctuation
import datetime

### load json file and return it as a workable string
def loadFile(f_to_load: str):
    """
        loadFile(f_to_load: str)

    This function will accept a file to load as a parameter. It implements a
    "try-catch" block to open the file passed as a parameter to the function
    when there is no error. It will then return the file's contents as a string
    to be worked with. When there is an error, the function will warn the user
    that the file could not be found, and then exit the program.
    """
    try:
        with open(f_to_load) as f:
            loaded_string: str = f.read()
            return loaded_string
    except:
        msg: str = f"\nThe specified file could not be found:\n\t{f_to_load}.\n"
        msg2: str = "Please check your path and try again."
        warn_msg: str = msg + msg2
        print(warn_msg)
        exit()


### parse the json data string read from the file into something that can work
parseJSON = lambda data_string: json.loads(data_string).get("roots")


def writeFile(string_to_write: str, outfile: str):
    """
    Function to write the markdown or org mode file to the disk.
    """
    with open(outfile, "w") as f:
        f.write(string_to_write)


###############################################################################
#                           POSTPROCESSING FUNCTIONS                                                                       #
###############################################################################


def post_process(
    file_to_process: str,
    in_format: str,
    out_format: str,
    outfile: str,
    keep_intermediate_file: bool = False,
):
    """
        post_process(file_to_process: str, in_format: str, out_format: str, outfile: str, keep_intermediate_file: bool = False)

    Function to run pandoc on the org mode or markdown file produced.
    'in-format' specifies the format of the file coming in (according to the
    value of the '-f' flag). 'out_format' specifies the format of the output
    file (ie. pdf, html). 'outfile' specifies the name for the output file.
    The value of 'keep_intermediate_file' determines whether or not the
    intermediate markdown or org mode file used as input for pandoc will be
    deleted after the completion of the program.
    """
    char_blacklist: set = set(punctuation)
    safe_out_format: str = "".join(
        char for char in out_format if char not in char_blacklist
    )
    if safe_out_format == "latex" or safe_out_format == "pdf":
        args: list[str] = [
            "pandoc",
            file_to_process,
            "-f",
            in_format,
            "-t",
            safe_out_format,
            "-o",
            outfile,
            "-V",  # latex variables to follow
            "documentclass:scrartcl",
            "-V",
            "geometry:margin=2cm",
            "-V",
            r"header_includes:\usepackage{hyperref}",
            "-V",
            r"header_includes:\hypersetup{colorlinks=true,urlcolor=cyan}",
        ]
    else:
        args = [
            "pandoc",
            file_to_process,
            "-f",
            in_format,
            "-t",
            safe_out_format,
            "--standalone",
            "-o",
            outfile,
        ]

    print()
    print("---------------- Info ----------------")
    print("Running pandoc with ARGS:")
    print(" ".join(args[1 : len(args)]))
    print()
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        print("Error occured while running command. Is pandoc installed?")
        exit()
    if not keep_intermediate_file:
        remove(file_to_process)
