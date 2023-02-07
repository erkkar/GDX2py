"""Module contains classes for handling GAMS symbols"""

__author__ = "Erkka Rinne"

from typing import Sequence, Mapping


class _GAMSSymbol(object):
    """Abstarct class for handling GAMS symbols

    Attributes:
        expl_text (str): Symbol explanatory text
    """

    def __init__(self, expl_text: str):
        """Class constructor

        Args:
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
            first_key = next(iter(keys))
        except TypeError:
            raise ValueError("Keys must be a sequence")
        except StopIteration:  # In case no data was given
            keys = list()
            first_key = None
        if isinstance(first_key, tuple):
            dimension = len(first_key)
            # Check consistency of the keys
            if not all(len(key) == dimension for key in iter(keys)):
                raise ValueError("Check consistency of the keys argument")
            else:
                self.dimension = dimension
        elif first_key is not None:
            self.dimension = 1
        else:
            self.dimension = None

        # Store keys
        self._keys = list(keys)
        self._size = len(keys)

        # Process domain information if given
        if domain:
            # Check that the given domain matches the dimension of the symbol
            if self.dimension is not None:
                try:
                    if len(domain) != self.dimension:
                        raise ValueError("Domain is inconsistent with the given values")
                except TypeError:
                    raise ValueError("Domain must be a sequence")
            else:
                # Interpret dimension from the domain
                self.dimension = len(domain)
            # Save the domain information
            self.domain = domain

        # Fallback to one-dimensional symbol if no other info available
        if self.dimension is None:
            self.dimension = 1

    def __len__(self):
        return self._size


class GAMSSet(_GAMSNDimSymbol):
    """Class for GAMS Sets

    Attributes:
        elements (list): Set elements
        expl_text (str): Set explanatory text
        assoc_texts (list): Set element associated texts
    """

    def __init__(
        self,
        keys: Sequence[tuple],
        domain: Sequence[str] = None,
        expl_text: str = '',
        assoc_texts: Sequence[str] = None,
    ):
        """Constructor for GAMSSet

        Args:
            keys: Sequence of tuples of strings for the keys
            domain (optional): Sequence of domain set names, use `None` for the universal set
            expl_text (optional): Explanatory text
            assoc_texts (optional): Set element associated texts

        Raises:
            ValueError
        """

        super().__init__(keys, domain, expl_text)
        self._type = 'Set'
        self._assoc_texts = None
        if assoc_texts is not None:
            try:
                len_assoc_texts = len(assoc_texts)
            except TypeError:
                raise ValueError("Associated texts must be a sequence")
            if len_assoc_texts != self._size:
                raise ValueError("Length of associated texts does not match the keys")
            else:
                self._assoc_texts = list(assoc_texts)

    @property
    def elements(self):
        return self._keys

    @property
    def assoc_texts(self):
        return self._assoc_texts

    def __iter__(self):
        self._iterator = iter(self._keys)
        return self

    def __next__(self):
        return next(self._iterator)


class GAMSScalar(_GAMSSymbol):
    """Class for GAMS Scalars (0-dimensional Parameters)

    Attributes:
        expl_text (str): Symbol explanatory text
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
    
    Attributes:
        domain (list): List of set names that make the domain of the symbol
        expl_text (str): Symbol explanatory text

    Methods:
        keys: Return a view to the symbol's keys
        values: Return a view to the symbol's values
    """

    def __init__(
        self,
        data: Mapping[tuple, float],
        domain: Sequence[str] = None,
        expl_text: str = '',
    ):
        """Constructor for GAMSParameter

        Args:
            data: Dictionay of keys and values
            domain (optional): List of domain set names, use `None` for the universal set
            expl_text (optional): Explanatory text

        Raises:
            ValueError
        """

        # Check arguments
        try:
            super().__init__(data.keys(), domain, expl_text)
        except AttributeError:
            raise ValueError("Data must be a mapping")
        self._type = 'Parameter'
        self._data = data

    def keys(self):
        return self._data.keys()

    def values(self):
        try:
            return self._data.values()
        except TypeError:  # Support self.data being a pandas.Series
            return self._data.values

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        self._iterator = iter(self._data.items())
        return self

    def __next__(self):
        key, val = next(self._iterator)
        return key, float(val)

    def to_pandas(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "This feature needs pandas package. "
                "Please use pip or conda to install pandas"
            )
        df = pd.Series(iter(self.values()), self.keys(), name=self.expl_text)
        if self.domain:
            if isinstance(df.index, pd.MultiIndex):
                df.index.names = self.domain
            else:
                df.index.name = self.domain[0]

        return df


class GAMSVariable(_GAMSNDimSymbol):
    """Class for GAMS Variables

    Attributes:
        domain (list): List of set names that make the domain of the symbol
        expl_text (str): Symbol explanatory text

    Methods:
        keys: Return a view to the symbol's keys
        values: Return a view to the symbol's values
    """

    def __init__(
            self,
            data: Mapping[tuple, float],
            domain: Sequence[str] = None,
            expl_text: str = '',
    ):
        """Constructor for GAMSParameter

        Args:
            data: Dictionay of keys and values
            domain (optional): List of domain set names, use `None` for the universal set
            expl_text (optional): Explanatory text

        Raises:
            ValueError
        """

        # Check arguments
        try:
            super().__init__(data.keys(), domain, expl_text)
        except AttributeError:
            raise ValueError("Data must be a mapping")
        self._type = 'Parameter'
        self._data = data

    def keys(self):
        return self._data.keys()

    def values(self):
        try:
            return self._data.values()
        except TypeError:  # Support self.data being a pandas.Series
            return self._data.values

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        self._iterator = iter(self._data.items())
        return self

    def __next__(self):
        key, val = next(self._iterator)
        return key, float(val)

    def to_pandas(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "This feature needs pandas package. "
                "Please use pip or conda to install pandas"
            )
        df = pd.DataFrame(iter(self.values()), self.keys())
        df.name = self.expl_text

        if self.domain:
            if isinstance(df.index, pd.MultiIndex):
                df.index.names = self.domain
            else:
                df.index.name = self.domain[0]

        return df