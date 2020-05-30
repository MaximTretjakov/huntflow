import argparse


def parser_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', metavar="", help='increase verbosity', required=True)
    parser.add_argument('-b', '--base_path', metavar="", help='increase verbosity', required=True)
    return parser.parse_args()
