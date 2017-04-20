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
    >>> with GdxFile('/path/to/gdx/file.gdx', mode='w') as f:
    >>>     sym1 = f['symb1']  # Get a symbol
    >>>     sym2 = sym1 * 2 
    >>>     f['sym2'] = sym2   # Set a symbol

Symbols are Pandas Series objects.
 

