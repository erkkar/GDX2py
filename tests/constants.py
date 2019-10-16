# 
"""
Constants for tests

See file 'data/example_data.gms' for the GAMS code used to create 
file 'data/example.gdx'.
"""
import sys
import math

SYMLIST = ['set1', 'set2', 'CONSTANT', 'par1', 'par2', 'par3']

SET1 = ['a', 'b', 'c', 'd']
SET1_TEXT = "A one-dimensional set"
SET1_ASSOC_TEXTS = ['alpha', 'beta', 'charlie', 'delta']

SET2 = [('a', 'foo'), ('b', 'bar'), ('c', 'baz')]
SET2_TEXT = "A multidimensional set"
SET2_DOMAIN = ['set1', None]

CONSTANT = 10
CONSTANT_TEXT = "A scalar"

PAR1 = {'a': 1, 'b': 2, 'c':3, 'd': 4}
PAR1_TEXT = "A one-dimensional parameter"
PAR1_DOMAIN = ['set1']

PAR2 = {('a', 'aaa'): 10, 
        ('b', 'bbb'): 20, 
        ('c', 'ccc'): 30}
PAR2_TEXT = "A multidimensional parameter"
PAR2_DOMAIN = ['set1', None]

PAR3 = {'na': math.nan, 'eps': sys.float_info.min, 'pinf': math.inf, 'ninf': -math.inf}