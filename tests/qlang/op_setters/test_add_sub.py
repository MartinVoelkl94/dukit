
import pytest
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



def test_add_cols1():
    code = r'name  %+=1 +str  %'
    result = df.dk.qr(code).result
    expected = get_df().rename(columns={'name': 'name1'})
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_add_cols2():
    code = r'name  /age  %+=1 +str   %'
    result = df.dk.qr(code).result
    mapping = {
        'name': 'name1',
        'age': 'age1',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_add_cols3():
    code = r"""
    name %+=1 +str
    'date of birth' %+=1 +str
    %
    """
    result = df.dk.qr(code).result
    mapping = {
        'name': 'name1',
        'date of birth': 'date of birth1',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_add_rows():
    code = r'%%+=1'
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = expected.index + 1
    assert_frame_equal(result, expected)




@pytest.mark.parametrize('code, col, vals, dtype, message', [

    (
        r'age  .toint  +=1',
        'age',
        [
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
        ],
        'Int64',
        None
    ),

    (
        r'age  +=1  +int',
        'age',
        [
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
        ],
        'Int64',
        None
    ),

    (
        r'age  +=1  +str',
        'age',
        [
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
        ],
        'string',
        None
    ),

    (
        r'name  +=_',
        'name',
        [
            'John Doe_',
            'Jane Smith_',
            'Alice Johnson_',
            'Bob Brown_',
            'eva white_',
            'Frank miller_',
            'Grace TAYLOR_',
            'Harry Clark_',
            'IVY GREEN_',
            'JAck Williams_',
            'john Doe_',
        ],
        'string',
        None
    ),

    (
        r'name  !+=_',
        'name',
        [
            '_John Doe',
            '_Jane Smith',
            '_Alice Johnson',
            '_Bob Brown',
            '_eva white',
            '_Frank miller',
            '_Grace TAYLOR',
            '_Harry Clark',
            '_IVY GREEN',
            '_JAck Williams',
            '_john Doe',
        ],
        'string',
        None
    ),

    (
        r'height  +=@weight +int',
        'height',
        [
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
        ],
        'Int64',
        None
    ),

    ])
def test_add_vals(code, col, vals, dtype, message):
    result = df.dk.qr(code).result
    expected = pd.DataFrame({col: vals}, dtype=dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



def test_add_error():
    log(clear=True)
    code = r'name  %!+=1'
    df.dk.qs(code)
    check_message('ERROR: cannot negate addition of a non-string value')



def test_sub_cols1():
    code = r'name  %-=me  %'
    result = df.dk.qr(code).result
    expected = get_df().rename(columns={'name': 'na'})
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_sub_cols2():
    code = r'name  /age  %-=e  %'
    result = df.dk.qr(code).result
    mapping = {
        'name': 'nam',
        'age': 'ag',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_sub_cols3():
    code = r"""
    name %-=e
    'date of birth' %-=" of birth"
    %
    """
    result = df.dk.qr(code).result
    mapping = {
        'name': 'nam',
        'date of birth': 'date',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_sub_rows():
    code = r'%%-=1'
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = expected.index - 1
    assert_frame_equal(result, expected)




@pytest.mark.parametrize('code, col, vals, dtype, message', [

    (
        r'age  .toint  -=1',
        'age',
        [
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
        ],
        'Int64',
        None
    ),
    (
        r'age  -=1  +int',
        'age',
        [
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
        ],
        'Int64',
        None
    ),

    (
        r'name  -=Doe',
        'name',
        [
            'John ',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john ',
        ],
        'string',
        None
    ),

    (
        r'name  -=" Doe"',
        'name',
        [
            'John',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john',
        ],
        'string',
        None
    ),

    (
        r'name  !-=John',
        'name',
        [
            ' Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ],
        'string',
        None
    ),

    (
        r'name  !-=john',
        'name',
        [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            ' Doe',
        ],
        'string',
        None
    ),

    (
        r'name  !-="john "',
        'name',
        [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'Doe',
        ],
        'string',
        None
    ),

    (
        r'height  -=@weight +int',
        'height',
        [
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
        ],
        'Int64',
        None
    ),

    ])
def test_sub_vals(code, col, vals, dtype, message):
    result = df.dk.qr(code).result
    expected = pd.DataFrame({col: vals}, dtype=dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



def test_sub_error():
    log(clear=True)
    code = r'name  %!-=1'
    df.dk.qs(code)
    check_message('ERROR: cannot negate substraction of a non-string value')
