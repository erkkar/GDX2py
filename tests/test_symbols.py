"""Tests for GAMSSets"""

import pytest

from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter
from .constants import (SET1, SET1_TEXT,
                        SET2,
                        CONSTANT, CONSTANT_TEXT,
                        PAR1, PAR1_DOMAIN, PAR1_TEXT,
                        PAR2, PAR2_DOMAIN, PAR2_TEXT,
)


def test_create_set():
    s = GAMSSet('set1', SET1)
    assert s.elements == SET1

def test_set_as_list():
    s = GAMSSet('set1', SET1)
    assert list(s) == SET1

def test_set_length():
    s = GAMSSet('set1', SET1)
    assert len(s) == len(SET1)

def test_create_set_without_domain():
    s = GAMSSet('set1', SET1)
    assert s.domain is None

def test_create_set_with_domain():
    domain = ['super']
    s = GAMSSet('set1', SET1, domain)
    assert s.domain == domain

def test_create_set_expl_text():
    s = GAMSSet('set1', SET1, expl_text=SET1_TEXT)
    assert s.expl_text == SET1_TEXT

def test_create_set_dimension():
    s = GAMSSet('set2', SET2)
    assert s.dimension == 2

def test_multidim_set_length():
    s = GAMSSet('set2', SET2)
    assert len(s) == len(SET2)

def test_create_set_multidim():
    s = GAMSSet('set2', SET2)
    assert s.elements == SET2

def test_create_set_multidim_fail():
    with pytest.raises(ValueError):
        GAMSSet('s', [('a', 'b'), ('c')])

def test_create_scalar():
    pi = GAMSScalar('pi', CONSTANT, expl_text=CONSTANT_TEXT)
    assert str(pi) == CONSTANT_TEXT
    
def test_scalar_value():
    pi = GAMSScalar('pi', CONSTANT)
    assert float(pi) == CONSTANT

def test_create_parameter():
    par = GAMSParameter('par', PAR1, expl_text=PAR1_TEXT)
    assert str(par) == PAR1_TEXT

def test_parameter_keys():
    par = GAMSParameter('par', PAR1)
    assert set(par.keys()) == set(PAR1.keys())

def test_parameter_values():
    par = GAMSParameter('par', PAR1)
    assert set(par.values()) == set(PAR1.values())

def test_parameter_values_get():
    par = GAMSParameter('par', PAR1)
    key = list(PAR1.keys())[0]
    assert par[key] == PAR1[key]

def test_create_multidim_parameter():
    par = GAMSParameter('par', PAR2)
    assert par.dimension == 2

def test_multidim_parameter_keys():
    par = GAMSParameter('par2', PAR2)
    assert set(par.keys()) == set(PAR2.keys())

def test_multidim_parameter_values():
    par = GAMSParameter('par', PAR2)
    assert set(par.values()) == set(PAR2.values())

def test_multidim_parameter_values_get():
    par = GAMSParameter('par', PAR2)
    key = list(PAR2.keys())[0]
    assert par[key] == PAR2[key]

def test_parameter_to_dict():
    par = GAMSParameter('par', PAR1)
    assert dict(par) == PAR1
    
