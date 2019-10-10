"""Tests for GAMSSets"""

import pytest

from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter


simple_list = ['a', 'b']
list_of_values = [1, 2]
domain = ['super']
list_of_tuples = [('a', 'b'), ('c', 'd')]
pi_value = 3.14


def test_create_set():
    s = GAMSSet('s', simple_list)
    assert s.elements == simple_list

def test_set_as_list():
    s = GAMSSet('s', simple_list)
    assert list(s) == simple_list

def test_set_length():
    s = GAMSSet('s', simple_list)
    assert len(s) == 2

def test_create_set_without_domain():
    s = GAMSSet('s', simple_list)
    assert s.domain is None

def test_create_set_with_domain():
    s = GAMSSet('s', simple_list, domain)
    assert s.domain == domain

def test_create_set_expl_text():
    expl_text = "My set"
    s = GAMSSet('s', simple_list, expl_text=expl_text)
    assert s.expl_text == expl_text

def test_create_set_dimension():
    s = GAMSSet('s', list_of_tuples)
    assert s.dimension == 2

def test_multidim_set_length():
    s = GAMSSet('s', list_of_tuples)
    assert len(s) == 2

def test_create_set_multidim():
    s = GAMSSet('s', list_of_tuples)
    assert s.elements == list_of_tuples

def test_create_set_multidim_fail():
    with pytest.raises(ValueError):
        GAMSSet('s', [('a', 'b'), ('c')])

def test_create_scalar():
    pi_text = 'Value of pi'
    pi = GAMSScalar('pi', pi_value, expl_text=pi_text)
    assert str(pi) == pi_text
    
def test_scalar_value():
    pi = GAMSScalar('pi', pi_value)
    assert float(pi) == 3.14

def test_create_parameter():
    text = "A parameter"
    par = GAMSParameter('par', simple_list, list_of_values, expl_text=text)
    assert str(par) == text

def test_parameter_keys():
    par = GAMSParameter('par', simple_list, list_of_values)
    assert list(par.keys()) == simple_list

def test_parameter_values():
    par = GAMSParameter('par', simple_list, list_of_values)
    assert list(par.values()) == list_of_values

def test_parameter_values_get():
    par = GAMSParameter('par', simple_list, list_of_values)
    assert par[simple_list[0]] == list_of_values[0]

def test_create_multidim_parameter():
    par = GAMSParameter('par', list_of_tuples, list_of_values)
    assert par.dimension == 2

def test_multidim_parameter_keys():
    par = GAMSParameter('par', list_of_tuples, list_of_values)
    assert list(par.keys()) == list_of_tuples

def test_multidim_parameter_values():
    par = GAMSParameter('par', list_of_tuples, list_of_values)
    assert list(par.values()) == list_of_values

def test_multidim_parameter_values_get():
    par = GAMSParameter('par', list_of_tuples, list_of_values)
    assert par[list_of_tuples[0]] == list_of_values[0]

def test_parameter_to_dict():
    par = GAMSParameter('par', simple_list, list_of_values)
    assert dict(par) == {key: value for key, value in zip(simple_list, list_of_values)}
    

if __name__ == '__main__':
    par = GAMSParameter('par', list_of_tuples, list_of_values)
    list(par.keys())
