# GDX2py

[![Documentation Status](https://readthedocs.org/projects/gdx2py/badge/?version=latest)](https://gdx2py.readthedocs.io/en/latest/?badge=latest)

Read and write GAMS Data eXchange (GDX) files using Python.

## Requirements

- GAMS: version 47.0 or higher
- Python: 3.8 or higher


### Installing GAMS

Get GAMS from [https://www.gams.com/download/](https://www.gams.com/download/) 
and install it to your system. No license is needed for the use of GDX libraries.


## Installation

Install with

    pip install gdx2py


## Usage

    >>> from gdx2py import GdxFile, GAMSSet, GAMSScalar, GAMSParameter
    >>> with GdxFile('/path/to/gdx/file.gdx', mode='w') as gdx:
    >>>     gdx['set1'] = ['a', 'b', 'c']  # Write a simple set
    >>>     set1 = gdx['set1']  # Read a symbol
    >>>     # Write a 2-dimensional set
    >>>     gdx['set2'] = [('a', 'foo'), ('b', 'bar'), ('c', 'baz')]
    >>>     # Write a scalar with explanatory text
    >>>     gdx['scalar'] = GAMSScalar(3.14, expl_text="Value of pi")  
    >>>     # Write a parameter with domain                                     
    >>>     gdx['par1'] = GAMSParameter({'a': 1, 'b': 2,  
                                         'c': 3, 'd': 4 }, 
                                        domain=['set1'])  

## Comparison to similar packages

Compared to other packages like [PyGDX](https://github.com/khaeru/py-gdx), [gdx-pandas](https://github.com/NREL/gdx-pandas), [gdxtools](https://github.com/boxblox/gdxtools) and [gdxpy](https://github.com/jackjackk/gdxpy), *GDX2py* relies 
only on the Python standard library and the low-level GDX API `gamsapi.core.gdx` module which is part of the GAMS 
Python API (`gamsapi`) available on PyPI.
 

<hr>
<center>
<table width=500px frame="none">
<tr>
<td valign="middle" width=100px>
<img src=https://europa.eu/european-union/sites/europaeu/files/docs/body/flag_yellow_low.jpg alt="EU emblem" width=100%></td>
<td valign="middle">This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 774629.</td>
</table>
</center>
