======
pydiff
======

.. image:: https://travis-ci.org/myint/pydiff.png?branch=master
    :target: https://travis-ci.org/myint/pydiff
    :alt: Build status

pydiff diffs Python code at the bytecode level. This is useful for checking for
changes to the actual code structure while ignoring formatting changes.


Installation
============

From pip::

    $ pip install --upgrade pydiff


Example
=======

``foo.py``:

.. code-block:: python

    import os, sys
    def main():

        x = len(sys.argv) + 100

        y            = x+77
        print(y)

``bar.py``:

.. code-block:: python

    import os
    import sys


    def main():
        x = len(sys.argv) + 101
        y = x + 77
        print(y)

``$ pydiff foo.py bar.py``:

.. code-block:: diff

    --- foo.py
    +++ bar.py
    @@ -87,7 +87,7 @@
                                 '<0>',
                                 '<0>',
                                 'RETURN_VALUE'],
    -                'co_consts': [None, 100, 77],
    +                'co_consts': [None, 101, 77],
                     'co_flags': 67,
                     'co_freevars': (),
                     'co_kwonlyargcount': 0,
