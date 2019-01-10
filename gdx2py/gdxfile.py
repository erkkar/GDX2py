# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 13:29:45 2015

@author: ererkka
"""

import sys
import os.path
from copy import copy
from warnings import warn

import pandas as pd
import numpy as np

from gdxcc import *

# String representations of API constants
TYPE_STR = {
    GMS_DT_SET: 'set',
    GMS_DT_PAR: 'parameter',
    GMS_DT_VAR: 'variable',
    GMS_DT_EQU: 'equation',
    GMS_DT_ALIAS: 'alias',
}

# Define data types
GDX_DTYPE_TEXT = 'U254'  # max. length for set associated text is 254 chars
GDX_DTYPE_LABEL = 'U63'  # max. length for set element label is 63 chars
GDX_DTYPE_NUM = 'f8'

# Python version of GAMS special values
SPECIAL_VALUES = {
    GMS_SV_UNDEF: np.nan,
    GMS_SV_NA   : np.nan,
    GMS_SV_PINF : np.inf,
    GMS_SV_MINF : -np.inf,
    GMS_SV_EPS  : np.finfo(GDX_DTYPE_NUM).eps,
    GMS_SV_ACR  : np.nan,
    GMS_SV_NAINT: np.nan,
}

GMS_USERINFO_SET_PARAMETER = 0  # UserInfo value for sets and parameters


class GdxFile(object):
    """Class for working with a gdx file

    Use subscripting (gdx_object['<symbolname>']) to get/set a GAMS set or
    parameter symbol as a Pandas Series object. The (MultiLevel) index of
    the series gives the set element names. For a GAMS set, the values are
    associated text labels.

    Parameters
    ----------
    name : str
        Gdx file name
    mode : str
        File open mode: 'r' for reading, 'w' for writing,
        'w+' for appending (replaces existing symbol)
    gams_dir : str, optional
        Location of GAMS installation directory

    Attributes
    ----------
    filename : str
        Absolute filename

    Raises
    ------
    RuntimeError
        Unable to load gdx library, invalid mode
    FileNotFoundError
        Input file not found
    ValueError
        Unsupported mode
    OSError
        Unable to read/write file
    Exception
        Other errors
    """

    def __init__(self, filename, mode='r', gams_dir=None):

        self._h = new_gdxHandle_tp()  # Create a gdx handle
        if gams_dir is None:
            ret, err = gdxCreate(self._h, GMS_SSSIZE)
        else:
            ret, err = gdxCreateD(self._h, gams_dir, GMS_SSSIZE)
        if ret == 0:
            raise RuntimeError(err)

        creator = 'Python {}'.format(sys.version)

        self.filename = os.path.abspath(filename)
        if mode == 'r':
            ret, errno = gdxOpenRead(self._h, self.filename)
        elif mode == 'w':
            ret, errno = gdxOpenWrite(self._h, self.filename, creator)
        elif mode == 'w+' or mode == 'a':
            ret, errno = gdxOpenAppend(self._h, self.filename, creator)
            # Fallback to creating a new file if not found
            if ret == 0 and errno == -100041:
                ret, errno = gdxOpenWrite(self._h, self.filename, creator)
        else:
            raise ValueError("Unsupported mode '{}'.".format(mode))
        self._mode = mode

        # Error checking
        if ret == 0:
            if errno == 2:
                raise FileNotFoundError(self.filename)
            else:
                raise OSError(gdxErrorStr(self._h, errno)[1])

        # Set up unique element map
        self._UEL_map = {}

        # Vectorize
        self._get_uel_string = np.vectorize(self._get_uel_string,
                                            otypes=[GDX_DTYPE_LABEL])
        self._get_set_assoc_text = np.vectorize(self._get_set_assoc_text,
                                                otypes=[GDX_DTYPE_TEXT])

    def __del__(self):
        gdxFree(self._h)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __repr__(self):
        return "GdxFile('{}', mode='{}')".format(self.filename, self._mode)

    def __str__(self):
        header = "GDX file at '{}'\n\n".format(self.filename)
        ret, sym_count, uel_count = gdxSystemInfo(self._h)
        line = "{:<4}{:20}{:5}{:3}\n"
        symbols = line.format('id','name','type','dim')
        symbols += (4 + 20 + 5 + 3) * '-' + '\n'
        for i in range(1, sym_count + 1):
            ret, sym, dim, symtype = gdxSymbolInfo(self._h, i)
            symbols += line.format(i, sym, TYPE_STR[symtype][0:3], dim)

        return header + symbols

    def __len__(self):
        ret, sym_count, uel_cnt = gdxSystemInfo(self._h)
        if ret:
            return sym_count
        else:
            return 0

    def close(self):
        gdxClose(self._h)

    def __getitem__(self, key):
        """Read a GAMS symbol as Pandas Series object
        """
        try:
            symno = int(key)
        except ValueError:
            symno = self._find_symbol(key)
        if symno is None:
            warn("Symbol '{}' not found!".format(key))
            return None
        else:
            return self._read_symbol(symno)

    def __setitem__(self, key, data):
        """Store Pandas Series object or a list of tuples into a GAMS symbol
        """
        if self._mode == 'r':
            raise IOError("Cannot write in mode '{}'".format(self._mode))
        else:
            if self._find_symbol(key) is not None:
                raise NotImplementedError("Cannot replace "
                                          "existing symbol '{}'".format(key))
            else:
                if isinstance(data, tuple):
                    indices, values = data
                elif isinstance(data, list):
                    # Try to convert a list (of tuples) into a pd.Series
                    indices = data
                    values = None
                if not isinstance(data, pd.core.series.Series):
                    try:
                        idx = pd.MultiIndex.from_tuples(indices)
                    except TypeError:
                        warn("Cannot interpret input data!")
                        return None
                    data = pd.Series(index=idx, data=values)
                else:
                    values = data.values

                if values is None or data.dtype == object:
                    self._write_symbol(GMS_DT_SET, key, data, data.name)
                else:
                    self._write_symbol(GMS_DT_PAR, key, data, data.name)

    def _find_symbol(self, name):
        """Find symbol number by name

        Parameters
        ----------
        name : str

        Returns
        -------
        symno : int
        """
        ret, symno = gdxFindSymbol(self._h, name)
        if ret > 0:
            return symno
        else:
            return None

    def _get_symname(self, symno):
        """Get symbol name for a number"""
        ret, sym, _, _ = gdxSymbolInfo(self._h, symno)
        if ret:
            return sym
        else:
            return None

    def _get_symtype(self, symno):
        """Get symbol type"""
        ret, _, _, symtype = gdxSymbolInfo(self._h, symno)
        if ret:
            return symtype
        else:
            return None

    def _get_expl_text(self, symno):
        ret, recs, user_info, expl_text = gdxSymbolInfoX(self._h, symno)
        if ret > 0:
            return expl_text.encode(errors='replace').decode()
        else:
            return None

    def _get_domain(self, symno):
        """Get domain for symbol"""
        ret, domain = gdxSymbolGetDomainX(self._h, symno)
        if ret:
            return domain
        else:
            return []

    def _convert_string_index(self, index_labels):
        recs = len(index_labels)
        dims = len(index_labels[0])
        indices = np.empty(recs, dtype=intArray)

        assert gdxUELRegisterRawStart(self._h)
        for i in range(recs):
            indices[i] = intArray(dims)
            for j in range(dims):
                try:
                    uel_idx = self._UEL_map[index_labels[i][j]]
                except KeyError:
                    gdxUELRegisterRaw(self._h, index_labels[i][j])
                    ret, uel_idx, high_map  = gdxUMUelInfo(self._h)
                    self._UEL_map[uel_idx] = index_labels[i][j]
                    self._UEL_map[index_labels[i][j]] = uel_idx
                finally:
                    indices[i][j] = uel_idx
        assert gdxUELRegisterDone(self._h)

        return indices

    def _get_uel_string(self, uel_nr):
        try:
            return self._UEL_map[uel_nr]
        except KeyError:
            ret, label, uel_map = gdxUMUelGet(self._h, uel_nr)
            if ret:
                self._UEL_map[uel_nr] = label
                self._UEL_map[label] = uel_nr
                return label
            else:
                return ''

    def _get_set_assoc_text(self, value):
        ret, assoc_text, node = gdxGetElemText(self._h, int(value))
        if ret:
            return assoc_text
        else:
            return None

    def _readstrstart(self, symno):
        """Start string reading at given symbol

        Parameters
        ----------
        symno : int
            Symbol number

        Returns
        -------
        rec : int
            Number of records available

        Raises
        ------
        Exception
        """
        ret, recs = gdxDataReadStrStart(self._h, symno)
        if not ret:
            raise Exception(gdxErrorStr(self._h, gdxGetLastError(self._h))[1])
        else:
            return recs

    def _readrawstart(self, symno):
        """Start raw mode reading at given symbol

        Parameters
        ----------
        symno : int
            Symbol number

        Returns
        -------
        rec : int
            Number of records available

        Raises
        ------
        Exception
        """
        ret, recs = gdxDataReadRawStart(self._h, symno)
        if not ret:
            raise Exception(gdxErrorStr(self._h, gdxGetLastError(self._h))[1])
        else:
            return recs

    def _writestrstart(self, symname, symtype, dim, expl_text = ""):
        """Start writing a symbol using strings

        Parameters
        ----------
        symname : str
            Symbol name
        symtype : str
            Type of the symbol
        dim : int
            Dimension of the symbol
        expl_text : str
            Symbol explanatory text

        Raises
        ------
        Exception
        """

        ret = gdxDataWriteStrStart(self._h, symname, expl_text,
                                   dim, symtype, GMS_USERINFO_SET_PARAMETER)
        if not ret:
            raise Exception(gdxErrorStr(self._h, gdxGetLastError(self._h))[1])
        else:
            return None

    def _writerawstart(self, symname, symtype, dim, expl_text = ""):
        """Start writing a symbol in raw mode

        Parameters
        ----------
        symname : str
            Symbol name
        symtype : str
            Type of the symbol
        dim : int
            Dimension of the symbol
        expl_text : str
            Symbol explanatory text


        Raises
        ------
        Exception
        """

        ret = gdxDataWriteRawStart(self._h, symname, expl_text,
                                   dim, symtype, GMS_USERINFO_SET_PARAMETER)
        if not ret:
            raise Exception(gdxErrorStr(self._h, gdxGetLastError(self._h))[1])
        else:
            return None


    def _read_symbol(self, symno):
        """Read a GAMS symbol as a Pandas Series object

        Parameters
        ----------
        symtype : int
            Symbol number

        """

        # Get symbol info
        ret, sym, dim, symtype = gdxSymbolInfo(self._h, symno)
        if not ret:
            warn("Symbol not found!")
            return None

        # Get domain of symbol
        domain = self._get_domain(symno)

        # Get length of longest label
        label_maxlen = gdxSymbIndxMaxLength(self._h, symno)[0]

        # Start reading symbol
#        recs = self._readrawstart(symno)
        recs = self._readstrstart(symno)

        # Initialize keys and values arrays
        keys = np.empty((recs, dim),
                        dtype='U{}'.format(label_maxlen))
        values = np.full((recs, GMS_VAL_MAX), fill_value=np.nan,
                         dtype=GDX_DTYPE_NUM)

        # Read GDX data
        for i in range(recs):
            ret, keys[i, :], values[i, :], afdim = gdxDataReadStr(self._h)
            #assert ret
            #DP = new_TDataStoreProc_tp()
            #ret = gdxDataReadRawFast(self._h, symno, DP)
        gdxDataReadDone(self._h)

        # Only take values for now
        values = values[:, GMS_VAL_LEVEL]

        # For sets, read associated text and replace as the value
        if symtype == GMS_DT_SET:
            if gdxSetHasText(self._h, symno):
                values = self._get_set_assoc_text(values)
            else:
                values.fill(np.nan)
        else:
            # Check for GAMS special values
            for sv in SPECIAL_VALUES:
                values[np.isclose(values, sv)] = SPECIAL_VALUES[sv]

        try:
            # Get string labels and build the index
            #idx = pd.MultiIndex.from_arrays(self._get_uel_string(keys).T)
            idx = pd.MultiIndex.from_arrays(keys.T)
        except ValueError:
            idx = None
        else:
            # Set index level names
            idx.names = [(d if d != '*' else None) for d in domain]

        # Return final Series
        return pd.Series(values, index=idx, name=self._get_expl_text(symno))

    def _write_symbol(self, symtype, symname, data, expl_text=None):
        """Write a Pandas series to a GAMS Set symbol

        Parameters
        ----------
        symtype : int
            GAMS data type number
        symname : str
            Symbol name
        data : pandas.core.series.Series
            Input data. See class docstring for more info.
        expl_text : str, optional
            Symbol explanatory text

        Raises
        ------
        RuntimeError
            Error registering set associated name to string table.
        Exception
            Other errors
        """

        # Get number of dimensions
        try:
            dims = len(data.index.levels)
        except AttributeError:
            dims = 1

        recs = len(data.index)

        keys = data.index.values
        values = data.values

        set_has_text = data.notnull().any()

        if expl_text is None:
            expl_text = ''

        # Begin writing to a symbol
        try:
            #self._writerawstart(symname, symtype, dims, expl_text)
            self._writestrstart(symname, symtype, dims, expl_text)
        except:
            raise

        # Define domain
        domain = [(d if d is not None else '*') for d in data.index.names]
        ret = gdxSymbolSetDomainX(self._h, self._find_symbol(symname), domain)
        if not ret:
            raise RuntimeError("Unable to set domain for symbol '{}'".format(symname))

        # Init value array
        value_arr = doubleArray(GMS_VAL_MAX)
        for i in range(recs):
            # For sets, register the associated text in the string table and
            # store index number as the value
            if symtype == GMS_DT_SET:
                if set_has_text and pd.notnull(values[i]):
                    assoc_text = copy(values[i])
                    ret, value_arr[GMS_VAL_LEVEL] = gdxAddSetText(self._h,
                                                               str(assoc_text))
                    if not ret:
                        warn("Unable to register string '{}' "
                             "to string table".format(assoc_text))
                else:
                    value_arr[GMS_VAL_LEVEL] = 0
            else:
                value_arr[GMS_VAL_LEVEL] = values[i]

            gdxDataWriteStr(self._h, [str(k) for k in keys[i]], value_arr)

        gdxDataWriteDone(self._h)

        return None
