# 
"""
Constants for tests
"""

import pandas as pd

"""
* GAMS code used to create 'data/example.gdx'

Set set1 "A one-dimensional set" / a 'alpha',
                                   b 'beta',
                                   c 'charlie',
                                   d 'delta' /;
Set set2(set1, *) "A multidimensional set" / a.foo, b.bar, c.baz /;
Scalar CONSTANT "A scalar" / 10 /;
Parameter par1(set1) "A one-dimensional parameter" /a 1, b 2, c 3, d 4 /;
Parameter par2(set1, *) "A multidimensional parameter" /a.aaa 10,
                                                        b.bbb 20,
                                                        c.ccc 30 /;
"""

SET1 = pd.Series(index=pd.MultiIndex.from_arrays([['a', 'b', 'c', 'd']]), 
                 data=['alpha', 'beta', 'charlie', 'delta'],
                 name="A one-dimensional set")
SET2 = pd.Series(index=pd.MultiIndex.from_tuples([('a', 'foo'), 
                                                  ('b', 'bar'), 
                                                  ('c', 'baz')],
                                                  names=['set1', None]),
                 dtype=float,
                 name="A multidimensional set")
CONSTANT = pd.Series(data=10, dtype=float, name="A scalar")
PAR1 = pd.Series(index=SET1.index, data=[1, 2, 3, 4], 
                 dtype=float, name="A one-dimensional parameter")
PAR2 = pd.Series(index=pd.MultiIndex.from_tuples([('a', 'aaa'), 
                                                  ('b', 'bbb'), 
                                                  ('c', 'ccc')],
                                                  names=['set1', None]),
                 data=[10, 20, 30], 
                 dtype=float, name="A one-dimensional parameter")