# GDX2py
Read and write GAMS Data eXchange (GDX) files using Python

## Installation
    python setup.py install

## Usage
    >>> from gdx2py import GdxFile
    >>> f = GdxFile('/path/to/gdx/file.gdx')
    >>> f['a_parameter']

Symbols are Pandas Series objects.
 

