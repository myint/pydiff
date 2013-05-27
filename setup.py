#!/usr/bin/env python

"""Setup for pydiff."""

from __future__ import unicode_literals

import ast
from distutils import core


def version():
    """Return version string."""
    with open('pydiff.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s


with open('README.rst') as readme:
    core.setup(name='pydiff',
               version=version(),
               description='Diffs two Python files at the bytecode level.',
               long_description=readme.read(),
               license='Expat License',
               author='Steven Myint',
               url='https://github.com/myint/pydiff',
               classifiers=['Intended Audience :: Developers',
                            'Environment :: Console',
                            'Programming Language :: Python :: 2.7',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.2',
                            'Programming Language :: Python :: 3.3',
                            'License :: OSI Approved :: MIT License'],
               keywords='diff, bytecode, python, whitespace, formatting',
               py_modules=['pydiff'],
               scripts=['pydiff'])
