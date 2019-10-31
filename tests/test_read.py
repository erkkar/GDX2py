import math

import pytest

from gdx2py.gdxfile import GdxFile
from gdx2py.gdxfile import EPS_VALUE
from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter
from .constants import (SET1, SET1_TEXT, SET1_ASSOC_TEXTS,
                        SET2, CONSTANT, CONSTANT_TEXT,
                        PAR1, PAR1_TEXT,
                        PAR2, PAR3,
                        SYMLIST
)


@pytest.fixture
def example_gdx(shared_datadir):
    with GdxFile(shared_datadir / 'example.gdx', 'r') as gdx:
        yield gdx

def compare_elements(gdx: GdxFile, symname: str, data: list):
    return list(gdx[symname]) == data

def compare_values(gdx: GdxFile, symname: str, data: dict):
    return dict(gdx[symname]) == data


def test_gdx_str(example_gdx):
    assert str(example_gdx) == f"GDX file at '{example_gdx.filename}'"

def test_gdx_len(example_gdx):
    assert len(example_gdx) == len(SYMLIST)

def test_gdx_contains(example_gdx):
    assert all(sym in example_gdx for sym in SYMLIST)

def test_gdx_keys(example_gdx):
    keys = example_gdx.keys()
    assert len(keys) == len(SYMLIST)
    assert all(sym in keys for sym in SYMLIST)
    assert list(keys) == SYMLIST

def test_iterate_gdx(example_gdx):
    first_symname, first_sym = next(iter(example_gdx))
    assert first_symname == 'set1'
    assert isinstance(first_sym, GAMSSet)

def test_read_1d_set(example_gdx):
    assert isinstance(example_gdx['set1'], GAMSSet)

def test_read_set_expl_text(example_gdx):
    assert example_gdx['set1'].expl_text == SET1_TEXT

def test_read_set_assoc_texts(example_gdx):
    assert example_gdx['set1'].assoc_texts == SET1_ASSOC_TEXTS

def test_1d_set_elements(example_gdx):
    assert compare_elements(example_gdx, 'set1', SET1)

def test_read_2d_set(example_gdx):
    assert isinstance(example_gdx['set2'], GAMSSet)

def test_2d_set_elements(example_gdx):
    assert compare_elements(example_gdx, 'set2', SET2)

def test_read_scalar(example_gdx):
    assert isinstance(example_gdx['constant'], GAMSScalar)

def test_scalar_value(example_gdx):
    assert float(example_gdx['constant']) == CONSTANT

def test_scalar_expl_text(example_gdx):
    assert example_gdx['constant'].expl_text == CONSTANT_TEXT

def test_read_1d_parameter(example_gdx):
    assert isinstance(example_gdx['par1'], GAMSParameter)

def test_parameter_expl_text(example_gdx):
    assert example_gdx['par1'].expl_text == PAR1_TEXT

def test_1d_parameter_values(example_gdx):
    assert compare_values(example_gdx, 'par1', PAR1)

def test_read_2d_parameter(example_gdx):
    assert isinstance(example_gdx['par2'], GAMSParameter)

def test_2d_parameter_values(example_gdx):
    assert compare_values(example_gdx, 'par2', PAR2)

def test_parameter_with_special_values(example_gdx):
    par = example_gdx['par3']
    assert math.isnan(par['na'])
    assert math.isclose(par['eps'], EPS_VALUE)
    assert math.isinf(par['pinf'])
    assert math.isinf(par['ninf'])

def test_read_not_found(example_gdx):
    with pytest.raises(KeyError):
        example_gdx['foobar']

def test_read_par_with_no_domain(example_gdx):
    assert example_gdx['par3'].domain is None

