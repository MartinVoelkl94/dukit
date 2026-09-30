
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



def test_cols1():
    code = r"""
    %.raw
    """
    result = df.dk.qr(code).result
    cols = [
        "'ID'",
        "'name'",
        "'date of birth'",
        "'age'",
        "'gender'",
        "'height'",
        "'weight'",
        "'bp systole'",
        "'bp diastole'",
        "'cholesterol'",
        "'diabetes'",
        "'dose'",
        ]
    expected = df.copy()
    expected.columns = pd.Series(cols).convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_rows1():
    code = r"""
    %%.raw
    """
    result = df.dk.qr(code).result
    cols = [
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        ]
    expected = df.copy()
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = pd.Series(cols).convert_dtypes()
    assert_frame_equal(result, expected)




def test_vals1():
    code = r"""
    age  .raw
    """
    result = df.dk.qr(code).result
    vals = [
        "-25",
        "'30'",
        "nan",
        "NaT",
        "'40.0'",
        "'forty-five'",
        "'nan'",
        "'unk'",
        "''",
        "'unknown'",
        "35",
        ]
    expected = pd.DataFrame({'age': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)

