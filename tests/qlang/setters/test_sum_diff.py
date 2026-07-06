
import pandas as pd
from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    qr,
    )



params = []
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




def test_sum_colref():
    code = r"""
    height  +=@weight +int
    """
    result = qr(df, code).result
    vals = [
        240,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        135,
        ]
    expected = pd.DataFrame({'height': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_sum_int1():
    code = r"""
    age  .toint  +=1
    """
    result = qr(df, code).result
    vals = [
        -24,
        31,
        pd.NA,
        pd.NA,
        41,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        36,
        ]
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_sum_int2():
    code = r"""
    age  +=1  +int
    """
    result = qr(df, code).result
    vals = [
        -24,
        31,
        pd.NA,
        pd.NA,
        41,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        36,
        ]
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_sum_str():
    code = r"""
    age  +=1  +str
    """
    result = qr(df, code).result
    vals = [
        '-251',
        '301',
        pd.NA,
        pd.NA,
        '40.01',
        'forty-five1',
        'nan1',
        'unk1',
        '1',
        'unknown1',
        '351',
        ]
    expected = pd.DataFrame({'age': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_diff_colref():
    code = r"""
    height  -=@weight +int
    """
    result = qr(df, code).result
    vals = [
        100,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        265,
        ]
    expected = pd.DataFrame({'height': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_diff_int():
    code = r"""
    age  -=1  +int
    """
    result = qr(df, code).result
    vals = [
        -26,
        29,
        pd.NA,
        pd.NA,
        39,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        pd.NA,
        34,
        ]
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
