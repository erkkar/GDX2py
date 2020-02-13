# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 15:04:05 2019

@author: ererkka
"""

import tempfile

import pytest

from gdx2py.gdxfile import GdxFile
from gdx2py.gams import GAMSSet, GAMSScalar, GAMSParameter
from .constants import (SET1, SET1_TEXT, 
                        SET2, SET2_DOMAIN, SET2_TEXT,
                        CONSTANT, 
                        PAR1, PAR1_DOMAIN, PAR1_TEXT,
                        PAR2, PAR2_DOMAIN, PAR2_TEXT,
                        PAR3
                       )
from .test_read import compare_elements, compare_values, example_gdx


def test_write_and_read(tmp_path):
    filepath = tmp_path / 'test.gdx'
    with GdxFile(filepath, mode='w') as gdx:
        gdx['set1'] = GAMSSet(SET1, expl_text=SET1_TEXT)
        gdx['set2'] = GAMSSet(SET2, SET2_DOMAIN, expl_text=SET1_TEXT)
        gdx['scalar'] = GAMSScalar(CONSTANT)
        gdx['par1'] = GAMSParameter(PAR1, domain=PAR1_DOMAIN, expl_text=PAR1_TEXT)
        gdx['par2'] = GAMSParameter(PAR2, domain=PAR2_DOMAIN, expl_text=PAR2_TEXT)
        gdx['par3'] = GAMSParameter(PAR3)

    with GdxFile(filepath, mode='r') as gdx:
        assert float(gdx['scalar']) == CONSTANT
        assert compare_elements(gdx, 'set1', SET1)
        assert compare_elements(gdx, 'set2', SET2)
        assert compare_values(gdx, 'par1', PAR1)
        assert compare_values(gdx, 'par2', PAR2)

def test_write_same_again(tmp_path):
    filepath = tmp_path / 'test.gdx'
    with GdxFile(filepath, mode='w') as gdx:
        gdx['set1'] = GAMSSet(SET1, expl_text=SET1_TEXT)
        with pytest.raises(NotImplementedError):
            gdx['set1'] = GAMSSet(SET1, expl_text=SET1_TEXT)

def test_try_write_when_reading(example_gdx):
        with pytest.raises(IOError):
            example_gdx['set1'] = GAMSSet(SET1, expl_text=SET1_TEXT)

def test_write_python_types(tmp_path):
    filepath = tmp_path / 'test.gdx'
    with GdxFile(filepath, mode='w') as gdx:
        gdx['set1'] = SET1
        gdx['scalar'] = CONSTANT
        gdx['par1'] = PAR1

    with GdxFile(filepath, mode='r') as gdx:
        assert float(gdx['scalar']) == CONSTANT
        assert compare_elements(gdx, 'set1', SET1)
        assert compare_values(gdx, 'par1', PAR1)
        


def test_write_empty(tmp_path):
    # filepath = tmp_path / 'test.gdx'
    filepath = 'c:/var/test.gdx'
    with GdxFile(filepath, mode='w') as gdx:
        gdx['set1'] = GAMSSet(list())
        gdx['par1'] = GAMSParameter(dict())
