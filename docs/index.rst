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

``GdxFile`` objects behave like dictionaries.
   
>>> from gdx2py import GdxFile, GAMSSet, GAMSScalar, GAMSParameter
>>> with GdxFile('/path/to/gdx/file.gdx', mode='w') as gdx:
>>>     gdx['set1'] = ['a', 'b', 'c']  # Write a simple set
>>>     set1 = gdx['set1']  # Read a symbol
>>>     # Write a 2-dimensional set
>>>     gdx['set2'] = [('a', 'foo'), ('b', 'bar'), ('c', 'baz')]
>>>     # Write a scalar with explanatory text
>>>     pi = GAMSScalar(3.14, expl_text="Value of pi")  
>>>     gdx['pi'] = pi

GAMS symbol objects
~~~~~~~~~~~~~~~~~~~
    
The symbol returned is either a ``GAMSSet``, ``GAMSParameter`` or 
``GAMSScalar``. You can convert them to Python built-ins.

>>> float(pi)
3.14
>>> list(set1)
['a', 'b', 'c']
>>> par = GAMSParameter({'a': 1, 'b': 2, 'c': 3, 'd': 4 })
>>> dict(par)
{'a': 1, 'b': 2, 'c': 3, 'd': 4 }

Symbol domains
''''''''''''''

GAMS sets and parameteres can also have a domain. Use the optional ``domain`` 
parameter to the constructor to define the domain.

>>> cats = GAMSSet(['jaguar', 'lion', 'tiger'], domain=['animals'])

The universal set ('*' in GAMS) means there is no specific domain. 
Use ``None`` for the universal set.

>>> set2d = GAMSSet([('a', 'foo'), ('b', 'bar'), ('c', 'baz')], domain=['abc', None])



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
