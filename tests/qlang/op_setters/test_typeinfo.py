
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )


df = get_df()

def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



def test_cols():
    code = r"""
    %.typeinfo
    """
    result = df.dk.qr(code).result
    cols = [
        "'ID' [str] 'ID'",
        "'name' [str] 'name'",
        "'date of birth' [str] 'date of birth'",
        "'age' [str] 'age'",
        "'gender' [str] 'gender'",
        "'height' [str] 'height'",
        "'weight' [str] 'weight'",
        "'bp systole' [str] 'bp systole'",
        "'bp diastole' [str] 'bp diastole'",
        "'cholesterol' [str] 'cholesterol'",
        "'diabetes' [str] 'diabetes'",
        "'dose' [str] 'dose'",
        ]
    expected = df.copy()
    expected.columns = pd.Series(cols).convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_rows():
    code = r"""
    %%.typeinfo
    """
    result = df.dk.qr(code).result
    cols = [
        '0 [int] 0',
        '1 [int] 1',
        '2 [int] 2',
        '3 [int] 3',
        '4 [int] 4',
        '5 [int] 5',
        '6 [int] 6',
        '7 [int] 7',
        '8 [int] 8',
        '9 [int] 9',
        '10 [int] 10',
        ]
    expected = df.copy()
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = pd.Series(cols).convert_dtypes()
    assert_frame_equal(result, expected)




def test_vals():
    code = r"""
    age  .typeinfo
    """
    result = df.dk.qr(code).result
    vals = [
        "-25 [int] -25",
        "'30' [int] 30",
        "nan [float] nan",
        "NaT [na] None",
        "'40.0' [float] 40.0",
        "'forty-five' [str] 'forty-five'",
        "'nan' [na] None",
        "'unk' [str] 'unk'",
        "'' [na] None",
        "'unknown' [str] 'unknown'",
        "35 [int] 35",
        ]
    expected = pd.DataFrame({'age': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
