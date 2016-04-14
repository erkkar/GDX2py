# GDX2py
Read and write GAMS Data eXchange (GDX) files using Python

## Requirements
Install [GAMS](https://www.gams.com/) and GAMS Data Exchange API for Python. 

### GAMS Data Exchange API
    > cd /path/to/GAMS/apifiles/Python/api
    > python gdxsetup.py install

## Installation
    python setup.py install

## Usage
    >>> from gdx2py import GdxFile
    >>> f = GdxFile('/path/to/gdx/file.gdx')
    >>> f['a_parameter']

Symbols are Pandas Series objects.
 

