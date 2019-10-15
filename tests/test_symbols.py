"""Tests for GAMSSets"""

import pytest

from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter
from .constants import (SET1, SET1_TEXT, SET1_ASSOC_TEXTS,
                        SET2,
                        CONSTANT, CONSTANT_TEXT,
                        PAR1, PAR1_DOMAIN, PAR1_TEXT,
                        PAR2, PAR2_DOMAIN, PAR2_TEXT,
)


def test_create_set():
    s = GAMSSet(SET1)
    assert s.elements == SET1

def test_set_as_list():
    s = GAMSSet(SET1)
    assert list(s) == SET1

def test_set_length():
    s = GAMSSet(SET1)
    assert len(s) == len(SET1)

def test_create_set_without_domain():
    s = GAMSSet(SET1)
    assert s.domain is None

def test_create_set_with_domain():
    domain = ['super']
    s = GAMSSet(SET1, domain)
    assert s.domain == domain

def test_create_set_expl_text():
    s = GAMSSet(SET1, expl_text=SET1_TEXT)
    assert s.expl_text == SET1_TEXT

def test_set_with_associated_texts():
    s = GAMSSet(SET1, assoc_texts=SET1_ASSOC_TEXTS)
    assert s.assoc_texts == SET1_ASSOC_TEXTS

def test_set_with_associated_texts_fail():
    with pytest.raises(ValueError):
        GAMSSet(SET1, assoc_texts=['alpha'])

def test_create_set_dimension():
    s = GAMSSet(SET2)
    assert s.dimension == 2

def test_multidim_set_length():
    s = GAMSSet(SET2)
    assert len(s) == len(SET2)

def test_create_set_multidim():
    s = GAMSSet(SET2)
    assert s.elements == SET2

def test_create_set_multidim_fail():
    with pytest.raises(ValueError):
        GAMSSet([('a', 'b'), ('c')])

def test_create_scalar():
    constant = GAMSScalar(CONSTANT, expl_text=CONSTANT_TEXT)
    assert constant.expl_text == CONSTANT_TEXT
    
def test_scalar_value():
    constant = GAMSScalar(CONSTANT)
    assert float(constant) == CONSTANT

def test_create_parameter():
    par = GAMSParameter(PAR1, expl_text=PAR1_TEXT)
    assert par.expl_text == PAR1_TEXT

def test_parameter_keys():
    par = GAMSParameter(PAR1)
    assert set(par.keys()) == set(PAR1.keys())

def test_parameter_values():
    par = GAMSParameter(PAR1)
    assert set(par.values()) == set(PAR1.values())

def test_parameter_values_get():
    par = GAMSParameter(PAR1)
    key = list(PAR1.keys())[0]
    assert par[key] == PAR1[key]

def test_create_multidim_parameter():
    par = GAMSParameter(PAR2)
    assert par.dimension == 2

def test_multidim_parameter_keys():
    par = GAMSParameter(PAR2)
    assert set(par.keys()) == set(PAR2.keys())

def test_multidim_parameter_values():
    par = GAMSParameter(PAR2)
    assert set(par.values()) == set(PAR2.values())

def test_multidim_parameter_values_get():
    par = GAMSParameter(PAR2)
    key = list(PAR2.keys())[0]
    assert par[key] == PAR2[key]

def test_parameter_to_dict():
    par = GAMSParameter(PAR1)
    assert dict(par) == PAR1
    
