#!/usr/bin/env python
from __future__ import print_function
import unittest
from wordSearch import replace_string
from wordSearch import search_file
from wordSearch import open_files
from io import BytesIO as StringIO
import io
import sys
import argparse


class TestSum(unittest.TestCase):
    def test_replace_string(self):
        output = replace_string('ttest', 1, 5, 'test')
        self.assertEqual(output, 't\x1b[44;33mtest\x1b[m')

    def test_search_file(self):
        output = self._search_data()
        self.assertEqual(output, '\n\nsearch/file.txt 8 : ttest\nsearch/file.txt 9 : ####2 ttest\n')

    def _search_data(self):
        args = argparse.Namespace(color=False, files=[], machine=False, regex='test', underscore=False)
        file_name = open('search/file.txt', 'r')
        args.files.append(file_name)
        if sys.version_info < (3, 0):
            captured_output = StringIO()
        else:
            captured_output = io.StringIO()
        sys.stdout = captured_output
        search_file(args.files, args.regex, args.machine, args.underscore, args.color)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def test_open_file_with_valid_file_name(self):
        object = open_files(['file.txt'])
        output = type(object)
        self.assertEqual(output, list)

    def test_open_file_with_not_valid_file_name(self):
        if sys.version_info < (3, 0):
            captured_output = StringIO()
        else:
            captured_output = io.StringIO()
        sys.stdout = captured_output
        open_files([''])
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue(), "I/O error(2): "
                                                     "No such file or directory\n\tIgnoring filename: ''\n")


if __name__ == '__main__':
    unittest.main()
