import math

import pytest

from gdx2py import GdxFile
from gdx2py.gdxfile import EPS_VALUE
from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter
from .constants import SET1, SET2, CONSTANT, PAR1, PAR2, PAR3


@pytest.fixture
def example_gdx(shared_datadir):
    with GdxFile(shared_datadir / 'example.gdx', 'r') as f:
        yield f

def compare_elements(gdx: GdxFile, symname: str, data: list):
    return list(gdx[symname]) == data

def compare_values(gdx: GdxFile, symname: str, data: dict):
    return dict(gdx[symname]) == data

def test_read_1d_set(example_gdx):
    assert isinstance(example_gdx['set1'], GAMSSet)

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

def test_read_1d_parameter(example_gdx):
    assert isinstance(example_gdx['par1'], GAMSParameter)

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

