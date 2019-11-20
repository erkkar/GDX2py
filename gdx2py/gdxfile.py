# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 13:29:45 2015

@author: ererkka
"""

import sys
import os.path
import math
from copy import copy
from warnings import warn
from collections.abc import Mapping, Sequence, KeysView, ValuesView

from gdxcc import GMS_VAL_LEVEL, GMS_DT_SET, GMS_DT_PAR
import gdxcc

from .gams import _GAMSSymbol, GAMSSet, GAMSScalar, GAMSParameter

# String representations of API constants
GMS_DTYPES = {
    'Set': GMS_DT_SET,
    'Parameter': GMS_DT_PAR,
    'Scalar': GMS_DT_PAR,
    # Not used at the moments
    #'Variable': GMS_DT_VAR,
    #'Equation': GMS_DT_EQU,
    #'Alias': GMS_DT_ALIAS:
}

# Define data types
GDX_DTYPE_TEXT = 'U254'  # max. length for set associated text is 254 chars
GDX_DTYPE_LABEL = 'U63'  # max. length for set element label is 63 chars
GDX_DTYPE_NUM = 'f8'

# Define Eps as the smalles float
EPS_VALUE = sys.float_info.min

# Python version of GAMS special values
SPECIAL_VALUES = {
    gdxcc.GMS_SV_UNDEF: math.nan,
    gdxcc.GMS_SV_NA: math.nan,
    gdxcc.GMS_SV_PINF: math.inf,
    gdxcc.GMS_SV_MINF: -math.inf,
    gdxcc.GMS_SV_EPS: EPS_VALUE,
    gdxcc.GMS_SV_ACR: math.nan,
    gdxcc.GMS_SV_NAINT: math.nan,
}

GMS_USERINFO_SET_PARAMETER = 0  # UserInfo value for sets and parameters


class GdxFile(object):
    """Class for working with a gdx file

    Use subscripting (gdx_object['<symbolname>']) to get/set a GAMS set or
    parameter symbol. 

    Attributes: 
        filename (str): Absolute filename
    """

    def __init__(self, filename: str, mode: str = 'r', gams_dir: str = None):
        """Constructor for GdxFile
        
        Args:
            filename: str
            mode: File open mode: 'r' for reading, 'w' for writing, 'w+' for appending (replaces existing symbol)
            gams_dir (optional): Location of GAMS installation directory

        Raises:
            RuntimeError: Unable to load gdx library, invalid mode
            FileNotFoundError: Input file not found
            ValueError: Unsupported mode
            OSError: Unable to read/write file
            Exception: Other errors
        """

        self._h = gdxcc.new_gdxHandle_tp()  # Create a gdx handle
        if gams_dir is None:
            ret, err = gdxcc.gdxCreate(self._h, gdxcc.GMS_SSSIZE)
        else:
            ret, err = gdxcc.gdxCreateD(self._h, gams_dir, gdxcc.GMS_SSSIZE)
        if ret == 0:
            raise RuntimeError(err)

        creator = 'Python {}'.format(sys.version)

        self.filename = os.path.abspath(filename)
        if mode == 'r':
            ret, errno = gdxcc.gdxOpenRead(self._h, self.filename)
        elif mode == 'w':
            ret, errno = gdxcc.gdxOpenWrite(self._h, self.filename, creator)
        elif mode == 'w+' or mode == 'a':
            ret, errno = gdxcc.gdxOpenAppend(self._h, self.filename, creator)
            # Fallback to creating a new file if not found
            if ret == 0 and errno == -100041:
                ret, errno = gdxcc.gdxOpenWrite(self._h, self.filename, creator)
        else:
            raise ValueError("Unsupported mode '{}'.".format(mode))
        self._mode = mode

        # Error checking
        if ret == 0:
            if errno == 2:
                raise FileNotFoundError(self.filename)
            else:
                raise OSError(gdxcc.gdxErrorStr(self._h, errno)[1])

        # Set up unique element map
        self._UEL_map = {}

        # TODO
        # self._get_uel_string = np.vectorize(self._get_uel_string,
        #                                    otypes=[GDX_DTYPE_LABEL])
        # self._get_set_assoc_text = np.vectorize(self._get_set_assoc_text,
        #                                        otypes=[GDX_DTYPE_TEXT])

    def __del__(self):
        gdxcc.gdxFree(self._h)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __repr__(self):
        return f"GdxFile('{self.filename}', mode='{self._mode}')"

    def __str__(self):
        return f"GDX file at '{self.filename}'"

    def __len__(self):
        ret, sym_count, _uel_cnt = gdxcc.gdxSystemInfo(self._h)
        if ret:
            return sym_count
        else:
            return 0

    def __contains__(self, symname):
        return True if self._find_symbol(symname) else False

    def keys(self):
        return _GdxKeysView(self)

    def close(self):
        gdxcc.gdxClose(self._h)

    def __getitem__(self, key):
        """Read a GAMS symbol from the gdx
        """
        try:
            symno = int(key)
        except ValueError:
            symno = self._find_symbol(key)
        if symno is None:
            raise KeyError(key)
        else:
            return self._read_symbol(symno)

    def __setitem__(self, name, data):
        """Store a GAMS Symbol object
        """
        if self._mode == 'r':
            raise IOError("Cannot write in mode '{}'".format(self._mode))
        elif self._find_symbol(name) is not None:
            raise NotImplementedError(
                "Cannot replace " "existing symbol '{}'".format(name)
            )

        # Try for a GAMSSymbol and different Python types
        if isinstance(data, _GAMSSymbol):
            symbol = data
        elif isinstance(data, Sequence):
            symbol = GAMSSet(data)
        elif isinstance(data, Mapping):
            symbol = GAMSParameter(data)
        elif isinstance(data, float) or isinstance(data, int):
            symbol = GAMSScalar(data)
        else:
            raise ValueError("Could not interpret given data as a GAMS symbol")

        self._write_symbol(name, symbol)

    @staticmethod
    def symrange(sym_count):
        return range(1, sym_count + 1)  # Skip symbol 0 which is the universal set

    def __iter__(self):
        self._iterator = iter(GdxFile.symrange(len(self)))
        return self

    def __next__(self):
        i = next(self._iterator)
        return self._get_symname(i), self[i]

    def _find_symbol(self, name: str) -> int:
        """Find symbol number by name

        Args:
            name: Symbol name
        """
        ret, symno = gdxcc.gdxFindSymbol(self._h, name)
        if ret > 0:
            return symno
        else:
            return None

    def _get_symname(self, symno):
        """Get symbol name for a number"""
        ret, sym, _, _ = gdxcc.gdxSymbolInfo(self._h, symno)
        if ret:
            return sym
        else:
            return None

    def _get_symtype(self, symno):
        """Get symbol type"""
        ret, _, _, symtype = gdxcc.gdxSymbolInfo(self._h, symno)
        if ret:
            return symtype
        else:
            return None

    def _get_expl_text(self, symno):
        ret, _recs, _user_info, expl_text = gdxcc.gdxSymbolInfoX(self._h, symno)
        if ret > 0:
            return expl_text.encode(errors='replace').decode()
        else:
            return None

    def _get_domain(self, symno):
        """Get domain for symbol"""
        ret, domain = gdxcc.gdxSymbolGetDomainX(self._h, symno)
        if ret:
            return domain
        else:
            return []

    def _convert_string_index(self, index_labels):
        pass  # TODO
        # recs = len(index_labels)
        # dims = len(index_labels[0])
        # #indices = np.empty(recs, dtype=intArray)

        # assert gdxcc.gdxUELRegisterRawStart(self._h)
        # for i in range(recs):
        #     indices[i] = gdxcc.intArray(dims)
        #     for j in range(dims):
        #         try:
        #             uel_idx = self._UEL_map[index_labels[i][j]]
        #         except KeyError:
        #             gdxcc.gdxUELRegisterRaw(self._h, index_labels[i][j])
        #             ret, uel_idx, high_map  = gdxcc.gdxUMUelInfo(self._h)
        #             self._UEL_map[uel_idx] = index_labels[i][j]
        #             self._UEL_map[index_labels[i][j]] = uel_idx
        #         finally:
        #             indices[i][j] = uel_idx
        # assert gdxcc.gdxUELRegisterDone(self._h)

        # return indices

    def _get_uel_string(self, uel_nr):
        try:
            return self._UEL_map[uel_nr]
        except KeyError:
            ret, label, _uel_map = gdxcc.gdxUMUelGet(self._h, uel_nr)
            if ret:
                self._UEL_map[uel_nr] = label
                self._UEL_map[label] = uel_nr
                return label
            else:
                return ''

    def _get_set_assoc_text(self, value):
        ret, assoc_text, _node = gdxcc.gdxGetElemText(self._h, int(value))
        if ret:
            return assoc_text
        else:
            return None

    def _read_symbol(self, symno: int):
        """Read a GAMS symbol as a Pandas Series object

        Args:
            symno: Symbol number

        Raises:
            RuntimeError
        """

        # Get symbol info
        ret, _sym, dim, symtype = gdxcc.gdxSymbolInfo(self._h, symno)
        if not ret:
            warn("Symbol not found!")
            return None

        # Get domain of symbol
        domain = [(d if d != '*' else None) for d in self._get_domain(symno)]
        if not any(domain):
            domain = None

        # Get explanatory text
        expl_text = self._get_expl_text(symno)

        # Get length of longest label
        _label_maxlen = gdxcc.gdxSymbIndxMaxLength(self._h, symno)[0]

        # Start reading symbol
        ret, recs = gdxcc.gdxDataReadStrStart(self._h, symno)
        if not ret:
            raise Exception(
                gdxcc.gdxErrorStr(self._h, gdxcc.gdxGetLastError(self._h))[1]
            )

        # Initialize keys and values arrays
        keys = recs * [tuple()]
        values = recs * [float()]
        if gdxcc.gdxSetHasText(self._h, symno):
            assoc_texts = recs * [str()]
        else:
            assoc_texts = None

        # Read GDX data
        # Code inside the loop is as small as possible for performance,
        # so the if statements are outside.
        if symtype == GMS_DT_SET and assoc_texts:
            for i in range(recs):
                _ret, key_arr, value_arr, _afdim = gdxcc.gdxDataReadStr(self._h)
                keys[i] = (
                    key_arr[0] if dim == 1 else tuple(key_arr)
                )  # Squeze out dimension of 1-dim keys
                assoc_texts[i] = self._get_set_assoc_text(value_arr[GMS_VAL_LEVEL])
        elif symtype == GMS_DT_SET and not assoc_texts:
            for i in range(recs):
                _ret, key_arr, _value_arr, _afdim = gdxcc.gdxDataReadStr(self._h)
                keys[i] = (
                    key_arr[0] if dim == 1 else tuple(key_arr)
                )  # Squeze out dimension of 1-dim keys
        elif symtype == GMS_DT_PAR:
            for i in range(recs):
                _ret, key_arr, value_arr, _afdim = gdxcc.gdxDataReadStr(self._h)
                keys[i] = (
                    key_arr[0] if dim == 1 else tuple(key_arr)
                )  # Squeze out dimension of 1-dim keys
                val = value_arr[GMS_VAL_LEVEL]
                values[i] = SPECIAL_VALUES.get(val, val)

        # Done reading
        gdxcc.gdxDataReadDone(self._h)

        # Construct GAMS symbols and return
        if symtype == GMS_DT_SET:
            return GAMSSet(keys, domain, expl_text=expl_text, assoc_texts=assoc_texts)
        elif symtype == GMS_DT_PAR:
            if dim == 0:
                return GAMSScalar(values[0], expl_text=expl_text)
            else:
                return GAMSParameter(
                    dict(zip(keys, values)), domain=domain, expl_text=expl_text
                )

    def _write_symbol(self, symname: str, symbol: _GAMSSymbol):
        """Write a Pandas series to a GAMS Set symbol

        Args:
            symbol: GAMS symbol object

        Raises:
            RuntimeError
        """

        # Get number of dimensions
        dim = symbol.dimension

        try:
            recs = len(symbol)
        except TypeError:
            recs = 1

        set_has_text = False  # TODO

        # Begin writing to a symbol
        ret = gdxcc.gdxDataWriteStrStart(
            self._h,
            symname,
            symbol.expl_text,
            dim,
            GMS_DTYPES[symbol._type],
            GMS_USERINFO_SET_PARAMETER,
        )
        if not ret:
            raise RuntimeError(
                gdxcc.gdxErrorStr(self._h, gdxcc.gdxGetLastError(self._h))[1]
            )

        # Define domain
        if symbol.domain is not None:
            domain = [(d if d is not None else '*') for d in symbol.domain]
        else:
            domain = dim * ['*']
        ret = gdxcc.gdxSymbolSetDomainX(self._h, self._find_symbol(symname), domain)
        if not ret:
            raise RuntimeError("Unable to set domain for symbol '{}'".format(symname))

        # Init value array
        value_arr = gdxcc.doubleArray(gdxcc.GMS_VAL_MAX)
        if dim == 0:  # It’s a scalar
            value_arr[GMS_VAL_LEVEL] = float(symbol)
            gdxcc.gdxDataWriteStr(self._h, list(), value_arr)
        elif isinstance(symbol, GAMSSet):
            for key in symbol:
                # For sets, register the associated text in the string table and
                # store index number as the value
                if set_has_text:
                    pass  # TODO
                    # assoc_text = copy(values[i])
                    # ret, value_arr[GMS_VAL_LEVEL] = gdxAddSetText(self._h,
                    #                                               str(assoc_text))
                    # if not ret:
                    #     warn("Unable to register string '{}' "
                    #          "to string table".format(assoc_text))
                else:
                    value_arr[GMS_VAL_LEVEL] = 0
                gdxcc.gdxDataWriteStr(self._h, list(key), value_arr)
        elif isinstance(symbol, GAMSParameter):
            for key, value in symbol:
                value_arr[GMS_VAL_LEVEL] = value
                gdxcc.gdxDataWriteStr(self._h, list(key), value_arr)

        gdxcc.gdxDataWriteDone(self._h)


class _GdxKeysView(KeysView):
    """Class for objects retuned by GdxFile.keys()
    """

    def __init__(self, gdx):
        self.gdx = gdx

    def __len__(self):
        return len(self.gdx)

    def __contains__(self, key):
        return key in self.gdx

    def __iter__(self):
        for i in GdxFile.symrange(len(self)):
            yield self.gdx._get_symname(i)


class _GdxSymbolsView(ValuesView):
    """Class for objects retuned by GdxFile.keys()
    """

    def __init__(self, gdx):
        self.gdx = gdx

    def __len__(self):
        return len(self.gdx)

    def __contains__(self, key):
        raise NotImplementedError()  # TODO

    def __iter__(self):
        for i in GdxFile.symrange(len(self)):
            yield self.gdx[i]
