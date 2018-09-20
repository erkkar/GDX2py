import pytest

from gdx2py import GdxFile

from constants import SET1, SET2, CONSTANT, PAR1, PAR2

@pytest.fixture
def gdx_file(shared_datadir):
    with GdxFile(shared_datadir / 'example.gdx', 'r') as f:
        yield f

def test_read_1d_set(gdx_file):
    assert gdx_file['set1'].equals(SET1)

def test_read_2d_set(gdx_file):
    assert gdx_file['set2'].equals(SET2)

def test_read_scalar(gdx_file):
    assert gdx_file['constant'].equals(CONSTANT)

def test_read_1d_parameter(gdx_file):
    assert gdx_file['par1'].equals(PAR1)

def test_read_2d_parameter(gdx_file):
    assert gdx_file['par2'].equals(PAR2)
