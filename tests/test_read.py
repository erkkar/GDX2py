import pytest

from gdx2py import GdxFile
from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter

from .constants import SET1, SET2, CONSTANT, PAR1, PAR2

@pytest.fixture
def gdx_file(shared_datadir):
    with GdxFile(shared_datadir / 'example.gdx', 'r') as f:
        yield f

def compare_elements(gdx: GdxFile, symname: str, data: list):
    return list(gdx[symname]) == data

def compare_values(gdx: GdxFile, symname: str, data: dict):
    return dict(gdx[symname]) == data

def test_read_1d_set(gdx_file):
    assert isinstance(gdx_file['set1'], GAMSSet)

def test_1d_set_elements(gdx_file):
    assert compare_elements(gdx_file, 'set1', SET1)

def test_read_2d_set(gdx_file):
    assert isinstance(gdx_file['set2'], GAMSSet)

def test_2d_set_elements(gdx_file):
    assert compare_elements(gdx_file, 'set2', SET2)

def test_read_scalar(gdx_file):
    assert isinstance(gdx_file['constant'], GAMSScalar)

def test_scalar_value(gdx_file):
    assert float(gdx_file['constant']) == CONSTANT

def test_read_1d_parameter(gdx_file):
    assert isinstance(gdx_file['par1'], GAMSParameter)

def test_1d_parameter_values(gdx_file):
    assert compare_values(gdx_file, 'par1', PAR1)

def test_read_2d_parameter(gdx_file):
    assert isinstance(gdx_file['par2'], GAMSParameter)

def test_2d_parameter_values(gdx_file):
    assert compare_values(gdx_file, 'par2', PAR2)

