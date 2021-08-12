import argparse


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--longer",
        dest="ex_arg",  # optional, would default to args.longer
        help="The help text.",
    )
    parser.add_argument(
        "-b",
        "--bool_flag",
        action="store_true",
        dest="ex_arg2",  # optional, would default to args.bool_flag
        help="help text",
    )
    return parser.parse_args()


def main():
    args = parse_commandline()


if __name__ == "__main__":
    main()
