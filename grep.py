#!/usr/bin/python3
import re, subprocess, sys
from os.path import realpath, isfile

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def python_grep(regex, file_path):
    """
    Search for regex in the lines of the given file
    and return a list of lines in which the regex is
    found.

    :param regex: regular expression string
    :type regex: str
    :param file_path: path to file
    :type file_path: str

    :returns: list of lines
    :rtype: list of str
    """

    RE = re.compile(regex)
    matching_lines = []
    if not isfile(file_path):
        raise FileNotFoundError("{} file was not found".format(file_path))
    for line in open(file_path):
        line = line.strip()
        if RE.search(line):
            matching_lines.append(line)
    return matching_lines


def grep_grep(regex, file_path):
    """
    Grep for a phrase in a given file and return the
    lines in which the regex is found.

    :param regex: regular expression string
    :type regex: str
    :param file_path: path to file
    :type file_path: str

    :returns: list of lines
    :rtype: list of str
    """
    matching_lines = []

    if not isfile(file_path):
        raise FileNotFoundError("{} file was not found".format(file_path))
    f = open(file_path, 'r')
    try:
        p = subprocess.check_output(['egrep', regex, file_path])
        p_decode = p.decode('utf-8')
        p_decode = list(p_decode.strip().split('\n'))
        for item in p_decode:
            matching_lines.append(item)
        return matching_lines
    except subprocess.CalledProcessError as e:
        if e.returncode > 1:
            raise e
        matching_lines = []
        return matching_lines

def main():
    parser = ArgumentParser(conflict_handler='resolve',
                            formatter_class=ArgumentDefaultsHelpFormatter,
                            description='Grep functionality in Python and'
                                        ' through Python.')
    parser.add_argument('-py', '--python',
                        help='Use Python to implement basic grep '
                             'functionality rather than calling grep.',
                        action='store_true',
                        default=False)
    parser.add_argument('regex',
                        help="Regular expression to search for.",
                        type=str)
    parser.add_argument('file',
                        help='File to grep in.',
                        type=str)
    args = parser.parse_args()

    file_path = realpath(args.file)

    if args.python:
        matching_lines = python_grep(args.regex, file_path)
    else:
        matching_lines = grep_grep(args.regex, file_path)

    for item in matching_lines:
        print(item)


if __name__ == "__main__":
    main()
