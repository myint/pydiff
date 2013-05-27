# Copyright (C) 2013 Steven Myint
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Diffs two Python files at the bytecode level."""

from __future__ import print_function
from __future__ import unicode_literals

import difflib
import pprint
import types


__version__ = '0.1'


def diff_bytecode_of_files(filename_a, filename_b):
    """Return diff of the bytecode of the two files."""
    with open_with_encoding(filename_a) as file_a:
        source_a = file_a.read()

    with open_with_encoding(filename_b) as file_b:
        source_b = file_b.read()

    return diff_bytecode(source_a, source_b)


def diff_bytecode(source_a, source_b):
    """Return diff of the bytecode of the two sources."""
    bytecode_a = disassemble(source_a)
    bytecode_b = disassemble(source_b)

    return ''.join(difflib.unified_diff(
        pprint.pformat(bytecode_a).splitlines(True),
        pprint.pformat(bytecode_b).splitlines(True))) + '\n'


def disassemble(source):
    """Return dictionary of disassembly."""
    return tree(compile(source, '<string>', 'exec'))


def tree(code):
    """Return dictionary representation of the code object."""
    dictionary = {'co_consts': []}
    for name in dir(code):
        if name.startswith('co_') and name not in ['co_code',
                                                   'co_consts',
                                                   'co_lnotab',
                                                   'co_filename',
                                                   'co_firstlineno']:
            dictionary[name] = getattr(code, name)

    for _object in code.co_consts:
        if isinstance(_object, types.CodeType):
            _object = tree(_object)

        dictionary['co_consts'].append(_object)

    return dictionary


def open_with_encoding(filename, encoding=None, mode='r'):
    """Return opened file with a specific encoding."""
    if not encoding:
        encoding = detect_encoding(filename)

    import io
    return io.open(filename, mode=mode, encoding=encoding,
                   newline='')  # Preserve line endings


def detect_encoding(filename):
    """Return file encoding."""
    try:
        with open(filename, 'rb') as input_file:
            from lib2to3.pgen2 import tokenize as lib2to3_tokenize
            encoding = lib2to3_tokenize.detect_encoding(input_file.readline)[0]

        # Check for correctness of encoding
        with open_with_encoding(filename, encoding) as test_file:
            test_file.read()

        return encoding
    except (LookupError, SyntaxError, UnicodeDecodeError):
        return 'latin-1'


def parse_args(argv):
    """Return parsed arguments."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, prog='pydiff')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('files', nargs=2,
                        help='files to compare')

    args = parser.parse_args(argv[1:])
    return args


def main(argv, standard_out):
    """Return exit status."""
    args = parse_args(argv)

    standard_out.write(diff_bytecode_of_files(args.files[0], args.files[1]))
