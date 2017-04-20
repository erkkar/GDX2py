# GDX2py
Read and write GAMS Data eXchange (GDX) files using Python

## Requirements
Install [GAMS](https://www.gams.com/) and GAMS Data Exchange API for Python. 

###GAMS Data Exchange API installation

    > cd /path/to/GAMS/apifiles/Python/api
    > python gdxsetup.py install

###Other dependencies
- Numpy: 1.8.1 or higher
- pandas: 0.17.1 or higher


## Installation

    python setup.py install

## Usage

    >>> from gdx2py import GdxFile
    >>> f = GdxFile('/path/to/gdx/file.gdx')
    >>> f['a_parameter']

Symbols are Pandas Series objects.
 

