"""Test pandas compatibility
"""

import pandas as pd

from gdx2py.gdxfile import GdxFile
from gdx2py.gams import GAMSParameter
from .constants import PAR1, PAR2, PAR1_TEXT


class TestPandas:
    def test_series(self):
        ts = pd.Series(PAR1)
        assert ts.to_dict() == dict(GAMSParameter(ts))

    def test_multi_index(self):
        ts = pd.Series(PAR2)
        assert ts.to_dict() == dict(GAMSParameter(ts))

    def test_series_from_parameter(self):
        ts = pd.Series(PAR1)
        par = GAMSParameter(PAR1)
        assert par.to_pandas().equals(ts)

    def test_series_name(self):
        par = GAMSParameter(PAR1, expl_text=PAR1_TEXT)
        assert par.to_pandas().name == PAR1_TEXT

    def test_write_series(self, tmp_path):
        filepath = tmp_path / 'test.gdx'
        ts = pd.Series(PAR1)
        with GdxFile(filepath, mode='w') as gdx:
            gdx['ts'] = GAMSParameter(ts)
