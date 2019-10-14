# 
"""
Constants for tests
"""


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