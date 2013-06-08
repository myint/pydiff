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

from __future__ import unicode_literals

import difflib
import opcode
import pprint
import types


try:
    basestring
except NameError:
    basestring = str


__version__ = '0.1.2'


class DisassembleSyntaxError(SyntaxError):

    """Raised if syntax error is detected while disassembling."""


def diff_bytecode_of_files(filename_a, filename_b):
    """Return diff of the bytecode of the two files."""
    with open_with_encoding(filename_a) as file_a:
        source_a = file_a.read()

    with open_with_encoding(filename_b) as file_b:
        source_b = file_b.read()

    return diff_bytecode(source_a, source_b,
                         filename_a, filename_b)


def diff_bytecode(source_a, source_b,
                  filename_a='', filename_b=''):
    """Return diff of the bytecode of the two sources."""
    bytecode_a = disassemble(source_a, filename_a)
    bytecode_b = disassemble(source_b, filename_b)

    return ''.join(difflib.unified_diff(
        pprint.pformat(bytecode_a).splitlines(True),
        pprint.pformat(bytecode_b).splitlines(True),
        filename_a,
        filename_b))


def disassemble(source, filename=''):
    """Return dictionary of disassembly."""
    try:
        return tree(compile(source, '<string>', 'exec', dont_inherit=True))
    except SyntaxError as syntax_error:
        exception = DisassembleSyntaxError()
        exception.filename = filename
        exception.msg = syntax_error.msg
        exception.text = syntax_error.text
        exception.lineno = syntax_error.lineno
        exception.offset = syntax_error.offset
        raise exception


def tree(code):
    """Return dictionary representation of the code object."""
    dictionary = {'co_consts': [],
                  'co_code': []}

    for name in dir(code):
        if name.startswith('co_') and name not in ['co_code',
                                                   'co_consts',
                                                   'co_lnotab',
                                                   'co_filename',
                                                   'co_firstlineno']:
            dictionary[name] = getattr(code, name)

    for index, _object in enumerate(code.co_consts):
        if isinstance(_object, types.CodeType):
            _object = tree(_object)

        # Ignore whitespace changes in docstrings.
        # We use 2 instead of 1 due to class names.
        if index < 2 and isinstance(_object, basestring):
            _object = ' '.join(
                [line.strip() for line in _object.splitlines()])

        dictionary['co_consts'].append(_object)

    for op in code.co_code:
        try:
            op = ord(op)
        except TypeError:
            pass

        dictionary['co_code'].append(opcode.opname[op])

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


def main(argv, standard_out, standard_error):
    """Return exit status."""
    args = parse_args(argv)

    try:
        diff = diff_bytecode_of_files(args.files[0], args.files[1])
        if diff:
            standard_out.write(diff + '\n')
    except DisassembleSyntaxError as exception:
        standard_error.write(
            '{0}:{1} invalid syntax\n'.format(
                exception.filename,
                exception.lineno))

        standard_error.write(str(exception.text))
        standard_error.write((exception.offset * ' ')[:-1] + '^\n')
