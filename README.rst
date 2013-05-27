======
pydiff
======

pydiff diffs Python code at the bytecode level. This is useful for checking for
changes to the actual code structure while ignoring formatting changes.


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

  ---
  +++
  @@ -4,7 +4,7 @@
                  None,
                  {'co_argcount': 0,
                   'co_cellvars': (),
  -                'co_consts': [None, 100, 77],
  +                'co_consts': [None, 101, 77],
                   'co_flags': 67,
                   'co_freevars': (),
                   'co_kwonlyargcount': 0,
