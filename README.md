# GDX2py

Read and write GAMS Data eXchange (GDX) files using Python


## Requirements

- GAMS: version 24.1 or higher
- Python: 3.6 or higher
- Numpy: 1.8.1 or higher
- pandas: 0.17.1 or higher
- GAMS Data Exchange API (gdxcc): 7.0 or higher


### Installing GAMS

Get GAMS from [https://www.gams.com/download/](https://www.gams.com/download/) 
and install it to your system. No license is needed for the use of GDX libraries.


### Other requirements

Install other requirements using

    pip install -r requirements.txt


## Installation

Install with

    pip install [-e] .
    
Use the `-e` switch to install in editable mode (for development).


## Usage

    >>> from gdx2py import GdxFile
    >>> with GdxFile('/path/to/gdx/file.gdx', mode='w') as f:
    >>>     sym1 = f['symb1']  # Get a symbol
    >>>     sym2 = sym1 * 2 
    >>>     f['sym2'] = sym2   # Set a symbol

Symbols are Pandas Series objects. Multidimensional sets or parameters are 
indexed with a MultiIndex. For sets, element explanatory text is stored as 
the Series data.
 

