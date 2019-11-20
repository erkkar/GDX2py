.. GDX2py documentation master file, created by
   sphinx-quickstart on Wed Nov 20 11:20:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GDX2py's documentation!
==================================

`GDX2py` is a Python package providing read and write support for GAMS GDX 
files using built-in data types list and dictionary.

.. toctree::
   :maxdepth: 1
   :caption: Contents:


Usage
-----

.. code-block:: python
    
    >>> from gdx2py import GdxFile, GAMSSet
    >>> with GdxFile('/path/to/gdx/file.gdx', mode='w') as f:
    >>>     sym1 = f['symb1']  # Read a symbol
    >>>     f['sym2'] = GAMSSet(['a', 'b', 'c'])  # Write a set
    >>>     f['sym2'] = GAMSParameter({'a': 1, 'b': 2, 'c': 3.5})  # Write a parameter


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
