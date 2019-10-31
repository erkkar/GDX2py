* GAMS code used to create 'data/example.gdx'

Set set1 "A one-dimensional set" / a 'alpha',
                                   b 'beta',
                                   c 'charlie',
                                   d 'delta' /;
Set set2(set1, *) "A multidimensional set" / a.foo 'foo of a'
                                             b.bar 'bar of b'
                                             c.baz 'baz of c' /;
Scalar CONSTANT "A scalar" / 10 /;
Parameter par1(set1) "A one-dimensional parameter" /a 1, b 2, c 3, d 4 /;
Parameter par2(set1, *) "A multidimensional parameter" /a.aaa 10,
                                                        b.bbb 20,
                                                        c.ccc 30 /;
Parameter par3(*) "Parameter with special values" / na na, eps Eps,
                                                    pinf Inf, ninf -Inf /
*execute_unload 'example.gdx';
