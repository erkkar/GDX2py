"""Module contains classes for handling GAMS symbols"""

from typing import Sequence, Mapping


class _GAMSSymbol(object):
    """Abstarct class for handling GAMS symbols

    Attributes:
        name (str): Symbol name
        expl_text (str): Symbol explanatory text
    """
    def __init__(self, expl_text: str):
        """Class constructor

        Args:
            name (str): Symbol name
            expl_text (str, optional): Symbol explanatory text
        """
        self.expl_text = expl_text
        self._type = None
        self.domain = None
        self.dimension = None


class _GAMSNDimSymbol(_GAMSSymbol):
    """Abstarct class for N-dimensional GAMS symbols
    """
    def __init__(self, keys: Sequence[tuple], domain: Sequence[str], expl_text: str):
        """Constructor for GAMSNDimSymbol

        Args:
            keys
            domain
            expl_text

        Raises:
            ValueError
        """

        super().__init__(expl_text)

        # Calculate dimension
        try:
            first_key = keys[0]
        except TypeError:
            raise ValueError("Keys must be a sequence")
        if isinstance(first_key, tuple):
            dimension = len(first_key)
            # Check consistency of the keys
            if not all(len(key) == dimension for key in keys):
                raise ValueError("Check consistency of the keys argument")
            else:
                self.dimension = dimension
        else:
            self.dimension = 1

        # Store keys
        self._keys = keys
        self._size = len(keys)

        # Check domain length
        if domain:
            try:
                if len(domain) != self.dimension:
                    raise ValueError("Domain is inconsistent with the given values")
            except TypeError:
                raise ValueError("Domain must be a sequence")
            self.domain = domain

    def __len__(self):
        return self._size


class GAMSSet(_GAMSNDimSymbol):
    """Class for GAMS Sets
    """
    def __init__(self, keys: Sequence[tuple], domain: Sequence[str] = None, 
                 expl_text: str = ''):
        """Constructor for GAMSSet

        Args:
            keys: Sequence of tuples of strings for the keys
            domain (optional): Sequence of domain set names
            expl_text (optional): Explanatory text

        Raises:
            ValueError
        """

        super().__init__(keys, domain, expl_text)
        self._type = 'Set'

    @property
    def elements(self):
        return self._keys

    def __iter__(self):
        self._iterator = iter(self._keys)
        return self

    def __next__(self):
        return next(self._iterator)


class GAMSScalar(_GAMSSymbol):
    """Class for GAMS Scalars (0-dimensional Parameters)
    """
    def __init__(self, value: float, expl_text: str = ''):
        """Class constructor

        Args:
            name: Symbol name
            value: Value

        Raises:
            ValueError
        """

        super().__init__(expl_text)
        self._type = 'Scalar'
        self.dimension = 0
        self._value = float(value)

    def __float__(self):
        return self._value
    
    def __int__(self):
        return int(self._value)


class GAMSParameter(_GAMSNDimSymbol):
    """Class for GAMS Parameters
    """

    def __init__(self, data: Mapping[tuple, float], domain: Sequence[str] = None, expl_text: str = ''):
        """Constructor for GAMSParameter

        Args:
            data: Dictionay of keys and values
            domain (optional): List of domain set names
            expl_text (optional): Explanatory text

        Raises:
            ValueError
        """

        # Check arguments
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        else:
            super().__init__(list(data.keys()), domain, expl_text)
            self._type = 'Parameter'
            self._data = data

    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()

    def __getitem__(self, key):
        return self._data[key]
    
    def __iter__(self):
        self._iterator = iter(self._data.items())
        return self

    def __next__(self):
        key, val = next(self._iterator)
        return key, float(val)
