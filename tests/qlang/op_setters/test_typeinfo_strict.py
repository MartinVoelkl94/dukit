
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
    %.typeinfo +strict
    """
    result = df.dk.qr(code).result
    cols = [
        "'ID' [str]",
        "'name' [str]",
        "'date of birth' [str]",
        "'age' [str]",
        "'gender' [str]",
        "'height' [str]",
        "'weight' [str]",
        "'bp systole' [str]",
        "'bp diastole' [str]",
        "'cholesterol' [str]",
        "'diabetes' [str]",
        "'dose' [str]",
        ]
    expected = df.copy()
    expected.columns = pd.Series(cols).convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_rows():
    code = r"""
    %%.typeinfo +strict
    """
    result = df.dk.qr(code).result
    cols = [
        '0 [int]',
        '1 [int]',
        '2 [int]',
        '3 [int]',
        '4 [int]',
        '5 [int]',
        '6 [int]',
        '7 [int]',
        '8 [int]',
        '9 [int]',
        '10 [int]',
        ]
    expected = df.copy()
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = pd.Series(cols).convert_dtypes()
    assert_frame_equal(result, expected)




def test_vals():
    code = r"""
    age  .typeinfo +strict
    """
    result = df.dk.qr(code).result
    vals = [
        "-25 [int]",
        "'30' [str]",
        "nan [float]",
        "NaT [NaTType]",
        "'40.0' [str]",
        "'forty-five' [str]",
        "'nan' [str]",
        "'unk' [str]",
        "'' [str]",
        "'unknown' [str]",
        "35 [int]",
        ]
    expected = pd.DataFrame({'age': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
