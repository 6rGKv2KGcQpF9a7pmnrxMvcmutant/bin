# What is this repo?

This is a repo with all my personal scripts that I use. Suggestions for
improving the scripts are welcome. As it's for my personal scripts, I
make no attempt to package the scripts that I use. However, I do try to
keep my scripts platform independent, so it should be relatively easy to
adapt any of these scripts for your own use.

# About the contents

## [agb_funcs.py](agb_funcs.py)

This file has helper functions for
[auto_gen_bookmarks.py](auto_gen_bookmarks.py). Each of the
three functions has docstrings, and you can see those for information on
the functions.

## [auto_gen_bookmarks.py](auto_gen_bookmarks.py)

This script reads the bookmarks stored by the [Brave
browser](https://brave.com/), and then generates an Emacs org-mode or
markdown file containing the bookmarks. The below shows usage
informaiton:

``` example
usage: auto_gen_bookmarks.py [-h] [-p PROFILE_NUM] [-o OUTFILE_NAME] [-m] [-P]
                             [-t PANDOC_OUT_FORMAT] [-k]

Program to read the JSON that the Brave browser stores its bookmarks info in
and create an org mode (or markdown) file containing said bookmarks from it.

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE_NUM, --profile_num PROFILE_NUM
                        The profile to take the bookmarks from. If zero is
                        entered, the program reads from the profile named
                        'Default'. This argument defaults to 0
  -o OUTFILE_NAME, --outfile_name OUTFILE_NAME
                        The name of the file produced by the script and
                        written to the disk.
  -m, --as_markdown     Make the file produced be in markdown format instead
                        of the default org-mode.
  -P, --post_process    Convert the file to some format after the markdown or
                        org mode document is produced. This uses the program
                        pandoc, and this functionality requires it as a
                        dependency.
  -t PANDOC_OUT_FORMAT, --pandoc_out_format PANDOC_OUT_FORMAT
                        Format to pass to pandoc as the type of the output
                        format. Suggestions are pdf, docx, html, and others
                        that play nicely with naming. Use in conjunction with
                        -P. This argument will default to html.
  -k, --keep_pp_file    This flag will cause the intermediate markdown or org
                        mode file produced to be kept. Use in conjunction with
                        -P.
```

## [get_sched_ss.py](get_sched_ss.py)

This is a script to get a screenshot of one's schedule using [George's
Schedule Machine](https://george.moe/imsa-scheduler/) and data from
one's SIS. It gets login info from [Bitwarden
CLI](https://github.com/bitwarden/cli), and then logs in to the user's
SIS with their credentials. *Note: to individualize this for your use,
be sure to change the mechanism for getting the login info, even if you
do use `bw`, as the way I have it configured, it queries using the
object ID, which is not portable.* Then, once obtaining the credentials,
it goes to George's Schedule Machine and inputs the schedule data,
saving screenshots of the table elements for the first and second
semester.

## [make_volunteer_hrs_entry.py](make_volunteer_hrs_entry.py)<span id="mvhe"></span>

This script is to automate the reporting of volunteer hours with
[HelperHelper](https://app.helperhelper.com/)<span id="hhlink"></span>.
It requires a TOML input file, which it then uses to enter the form
information into [HelperHelper](#hhlink).

``` example
usage: make_volunteer_hrs_entry.py [-h] [-i INPUT_FILE] [-H]

Program to automate the reporting of volunteer hours for IMSA using Selenium
and TOML.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        The TOML file to read as input containing the relevant
                        information to be inputed in their fields. See
                        ~/bin/mvhe/example.toml for an example.
  -H, --headful         Run the selenium webdriver in headful mode, opening
                        the browser so that the user can see what's happening.
```

## Directories

### [mvhe](mvhe)

This directory has a template and an example of the TOML used by the
[make_volunteerhrs_entry.py](#mvhe) script.
[example.toml](mvhe/example.toml) contains an example, while
[template.toml](mvhe/template.toml) contains basically the same file
with the fields replace by easily searchable placeholders. Each field
name corresponds with the corresponding field name in the
[HelperHelper](#hhlink) volunteer form.

### [.templates](.templates)

The files in this directory are templates for the scripts I make. The
names are self-explanatory.
