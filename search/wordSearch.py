#!/usr/bin/env python
from __future__ import print_function
import argparse
import re
import sys
import sre_constants

# script accepts list of files and a regular expression then searches for a matching pattern
# Author: Alekhya Gudimetla
# Examples:
#   ./wordSearch.py filename.txt filename2.txt regex
# Required parameters:
#    files       list of file names
#   regex       write regular expression in quotes
# optional arguments:
#   -h, --help             show this help message and exit
#   -m, --machine          machine readable format
#   -c, --color            highlight matching text
#   -u, --underscore       prints "^" under the matching text


def main():

    parser = argparse.ArgumentParser(description='reading a list of files and returning lines that match pattern')
    parser.add_argument('files', nargs='*', help='list of file names')
    parser.add_argument('regex', help='write regular expression in quotes')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--machine', action='store_true', help='machine readable format')
    group.add_argument('-c', '--color', action='store_true', help='highlight matching text')
    group.add_argument('-u', '--underscore',  action='store_true', help='prints "^" under the matching text')

    args = parser.parse_args()

    stdin_files_list = []
    for filename in args.files:
        if filename in ['', '-']:
            args.files.remove(filename)
            stdin_files_list.extend(get_filenames_from_stdin())
            if not stdin_files_list:
                print("\nWarning: No filenames provided via STDIN.")

    if stdin_files_list:
        args.files.extend(stdin_files_list)

    if not args.files:
        print("No files provided for searching.")
        sys.exit(1)

    file_handle_list = open_files(args.files)
    search_file(files=file_handle_list, regex=args.regex, machine_format=args.machine,
                color=args.color, underscore=args.underscore)


def open_files(file_list):

    file_obj_list = []
    for filename in file_list:
        try:
            file_obj_list.append(open(filename, 'r'))

        except IOError as e:
            errno, strerror = e.args
            print("I/O error({0}): {1}".format(errno, strerror))
            print("\tIgnoring filename: '{0}'".format(filename))

    return file_obj_list


def get_filenames_from_stdin():

    filenames = []
    ctrl_c_detected = False
    print('Enter file name (CTRL-C to exit): ')
    while not ctrl_c_detected:
        try:
            fn = sys.stdin.readline().strip()
            filenames.append(fn)
        except KeyboardInterrupt:
            ctrl_c_detected = True
    return filenames


def search_file(files, regex, machine_format=False, color=False, underscore=False):
    flag = False
    print("\n")
    for open_file in files:
        for index, line in enumerate(open_file, start=1):
            try:
                matches = re.finditer(regex,line)
            except sre_constants.error:
                print("Illegal regular expression: '{0}'".format(regex))
                return

            for match_obj in matches:
                word = match_obj.group(0)
                start_pos = match_obj.start()
                end_pos = match_obj.end()

                if word:
                    if machine_format:
                        print(open_file.name, ':',  index, ':', start_pos + 1, ':', line.strip())

                    elif color:
                        print(open_file.name, index, ':',
                              replace_string(line.strip(), start_pos, end_pos, word))

                    elif underscore:
                        delimiter = " : "
                        delimiter_chars = len(delimiter) * 2
                        # to provide starting position for matching text
                        start_pos_match = (len(open_file.name) + start_pos + delimiter_chars +
                                           len(str(index)) + len(word))
                        spaces = '{:>' + str(start_pos_match) + '}'
                        print("{file}{delimiter}{index}{delimiter}{line}\n{underscore}".format(
                            file=open_file.name, index=index, line=line.strip(), delimiter=delimiter,
                            underscore=spaces.format('^' * (len(word)))))

                    else:
                        print(open_file.name, index, ':', line.strip())

                    flag = True


        if not flag:
            print('Match is not found in file', open_file.name)


def replace_string(line, start_pos, end_pos, word):
    return line[:start_pos] + '\033[44;33m{}\033[m'.format(word) + line[end_pos:]


if __name__ == '__main__':
    main()
