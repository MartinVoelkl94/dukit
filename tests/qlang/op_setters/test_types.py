
import pytest
import numpy as np
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




def test_all_vals_toint():
    code = r"""
    %%% .toint()
    """
    result = df.dk.qr(code).result
    data = {}
    data['ID'] = [
        10001,
        10002,
        10003,
        20001,
        20002,
        20003,
        30001,
        30002,
        30003,
        30004,
        30005,
        ]
    data['name'] = [np.nan] * 11
    data['date of birth'] = [np.nan] * 11
    data['date of birth'][3] = 19800406
    data['age'] = [
        -25,
        30,
        np.nan,
        np.nan,
        40,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        35,
        ]
    data['gender'] = [np.nan] * 11
    data['height'] = [
        170,
        np.nan,
        np.nan,
        280,
        np.nan,
        185,
        1,
        np.nan,
        -10,
        np.nan,
        200,
        ]
    data['weight'] = [
        70,
        68,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        80,
        np.nan,
        100,
        -65,
        ]
    data['bp systole'] = [
        20,
        130,
        np.nan,
        np.nan,
        np.nan,
        126,
        np.nan,
        122,
        np.nan,
        130,
        45,
        ]
    data['bp diastole'] = [
        80,
        85,
        np.nan,
        np.nan,
        np.nan,
        75,
        np.nan,
        np.nan,
        95,
        0,
        np.nan,
        ]
    data['cholesterol'] = [np.nan] * 11
    data['diabetes'] = [
        np.nan,
        np.nan,
        np.nan,
        0,
        1,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        ]
    data['dose'] = [np.nan] * 11
    data['dose'][9] = 35
    expected = pd.DataFrame(data, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_raw_rep_cols():
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




def test_raw_rep_rows():
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




def test_raw_rep_vals():
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




@pytest.mark.parametrize('code, vals, col, dtype', [

    #obj
    (
        r'age  .toobj()',
        [
            -25,
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            35,
        ],
        'age',
        'object',
    ),

    #str
    (
        r'age  .tostr()',
        [
            '-25',
            '30',
            pd.NA,
            pd.NA,
            '40.0',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            '35',
        ],
        'age',
        'string',
    ),
    (
        r'"date of birth"  .tostr()',
        [
            '1995-01-02 00:00:00',
            '1990-09-14 00:00:00',
            '1985.08.23',
            '19800406',
            '05-11-2007',
            '1983-06-30',
            '1975-05-28',
            '1960Mar08',
            '1955-Jan-09',
            '1950 Sep 10',
            '1945 October 11',
        ],
        'date of birth',
        'string',
    ),

    #int
    (
        r'name  .toint()',
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        'name',
        'Int64',
    ),
    (
        r'name  %%%.toint()',
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        'name',
        'Int64',
    ),
    (
        r'weight .toint()',
        [
            70.0,
            68,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            80.0,
            np.nan,
            100,
            -65,
        ],
        'weight',
        'Int64',
    ),
    (
        r'weight %%>70 .toint()  %%',
        [
            70,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            80,
            '130lbs',
            100,
            -65,
        ],
        'weight',
        'object',
    ),
    (
        r'name  .tofloat()',
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        'name',
        'Float64',
    ),
    (
        r'weight .tofloat()',
        [
            70.2,
            68,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            80.3,
            np.nan,
            100,
            -65,
        ],
        'weight',
        'Float64',
    ),

    #float
    (
        r'weight %%>70 .tofloat()  %%',
        [
            70.2,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            80.3,
            '130lbs',
            100.0,
            -65,
        ],
        'weight',
        'object',
    ),
    (
        r'weight  %%>70  %%%.tofloat()  %%',
        [
            70.2,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            80.3,
            '130lbs',
            100.0,
            -65,
        ],
        'weight',
        'object',
    ),

    #num
    (
        r'name  .tonum()',
        [
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
        ],
        'name',
        'Int64',
    ),
    (
        r'weight .tonum()',
        [
            70.2,
            68,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            80.3,
            pd.NA,
            100,
            -65,
        ],
        'weight',
        'Float64',
    ),
    (
        r'weight %%>70 .tonum()  %%',
        [
            70.2,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            80.3,
            '130lbs',
            100,
            -65,
        ],
        'weight',
        'object',
    ),
    (
        r'weight  %%>70  %%%.tonum()  %%',
        [
            70.2,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            80.3,
            '130lbs',
            100,
            -65,
        ],
        'weight',
        'object',
    ),

    #bool
    (
        r'name  .tobool()',
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ],
        'name',
        'boolean',
    ),
    (
        r'diabetes  .tobool()',
        [
            False,
            True,
            None,
            False,
            True,
            True,
            False,
            None,
            None,
            False,
            True,
        ],
        'diabetes',
        'boolean',
    ),
    (
        r'diabetes  :isyn() .tobool()  %%',
        [
            False,
            True,
            'N/A',
            False,
            True,
            True,
            False,
            None,
            'NaN',
            False,
            True,
        ],
        'diabetes',
        'object',
    ),
    (
        r'diabetes  %%:isyn()  %%%.tobool()  %%',
        [
            False,
            True,
            'N/A',
            False,
            True,
            True,
            False,
            None,
            'NaN',
            False,
            True,
        ],
        'diabetes',
        'object',
    ),

    #date
    (
        r'name  .todate()',
        [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        'name',
        'datetime64[s]',
    ),
    (
        r'"date of birth"  .todate()',
        [
            pd.to_datetime('1995-01-02').date(),
            pd.to_datetime('1990-09-14').date(),
            pd.to_datetime('1985-08-23').date(),
            pd.to_datetime('1980-04-06').date(),
            pd.to_datetime('2007-11-05').date(),
            pd.to_datetime('1983-06-30').date(),
            pd.to_datetime('1975-05-28').date(),
            pd.to_datetime('1960-03-08').date(),
            pd.to_datetime('1955-01-09').date(),
            pd.to_datetime('1950-09-10').date(),
            pd.to_datetime('1945-10-11').date(),
        ],
        'date of birth',
        'object',
    ),
    (
        r'"date of birth"  %%!:isint() .todate()  %%',
        [
            pd.to_datetime('1995-01-02').date(),
            pd.to_datetime('1990-09-14').date(),
            pd.to_datetime('1985-08-23').date(),
            '19800406',
            pd.to_datetime('2007-11-05').date(),
            pd.to_datetime('1983-06-30').date(),
            pd.to_datetime('1975-05-28').date(),
            pd.to_datetime('1960-03-08').date(),
            pd.to_datetime('1955-01-09').date(),
            pd.to_datetime('1950-09-10').date(),
            pd.to_datetime('1945-10-11').date(),
        ],
        'date of birth',
        'object',
    ),

    #datetime
    (
        r'name  .todatetime()',
        [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        'name',
        'datetime64[us]',
    ),
    (
        r'"date of birth"  .todatetime()',
        [
            '1995-01-02',
            '1990-09-14',
            '1985-08-23',
            '1980-04-06',
            '2007-11-05',
            '1983-06-30',
            '1975-05-28',
            '1960-03-08',
            '1955-01-09',
            '1950-09-10',
            '1945-10-11',
        ],
        'date of birth',
        'datetime64[us]',
    ),
    (
        r'"date of birth"  %%!:isint() .todatetime()  %%',
        [
            pd.to_datetime('1995-01-02'),
            pd.to_datetime('1990-09-14'),
            pd.to_datetime('1985-08-23'),
            '19800406',
            pd.to_datetime('2007-11-05'),
            pd.to_datetime('1983-06-30'),
            pd.to_datetime('1975-05-28'),
            pd.to_datetime('1960-03-08'),
            pd.to_datetime('1955-01-09'),
            pd.to_datetime('1950-09-10'),
            pd.to_datetime('1945-10-11'),
        ],
        'date of birth',
        'object',
    ),
    (
        r'"date of birth"  %%!:isint() .todatetime()  %%',
        [
            pd.to_datetime('1995-01-02'),
            pd.to_datetime('1990-09-14'),
            pd.to_datetime('1985-08-23'),
            '19800406',
            pd.to_datetime('2007-11-05'),
            pd.to_datetime('1983-06-30'),
            pd.to_datetime('1975-05-28'),
            pd.to_datetime('1960-03-08'),
            pd.to_datetime('1955-01-09'),
            pd.to_datetime('1950-09-10'),
            pd.to_datetime('1945-10-11'),
        ],
        'date of birth',
        'object',
    ),

    #na
    (
        r'name .tona()',
        df['name'].tolist(),
        'name',
        'string',
    ),
    (
        r'diabetes  .tona()',
        [
            False,
            'true',
            None,
            0,
            '1',
            'Yes',
            'NO',
            None,
            None,
            'n',
            True,
        ],
        'diabetes',
        'object',
    ),
    (
        r'diabetes  %%!?"/"  .tona()  %%',
        [
            False,
            'true',
            'N/A',
            0,
            '1',
            'Yes',
            'NO',
            None,
            None,
            'n',
            True,
        ],
        'diabetes',
        'object',
    ),
    (
        r'diabetes  %%!?"/"  %%%.tona() %%',
        [
            False,
            'true',
            'N/A',
            0,
            '1',
            'Yes',
            'NO',
            None,
            None,
            'n',
            True,
        ],
        'diabetes',
        'object',
    ),

    #nk
    (
        r'age  .tonk()',
        [
            -25,
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unknown',
            '',
            'unknown',
            35,
        ],
        'age',
        'object',
    ),
    (
        r'age  :!>0  .tonk()  %%',
        [
            -25,
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unknown',
            '',
            'unknown',
            35,
        ],
        'age',
        'object',
    ),

    #yn
    (
        r'diabetes  .toyn()',
        [
            'no',
            'yes',
            pd.NA,
            'no',
            'yes',
            'yes',
            'no',
            pd.NA,
            pd.NA,
            'no',
            'yes',
        ],
        'diabetes',
        'string',
    ),
    (
        r'diabetes  !=7 +index  .toyn()  %%',
        [
            'no',
            'yes',
            pd.NA,
            'no',
            'yes',
            'yes',
            'no',
            None,
            pd.NA,
            'no',
            'yes',
        ],
        'diabetes',
        'object',
    ),

    ])
def test_set_vals(code, vals, col, dtype):
    result = df.dk.qr(code).result
    expected = pd.DataFrame({col: vals}, dtype=dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




@pytest.mark.parametrize('code, error_type', [
    (
        r'weight .toint(+strict)',
        ValueError,
    ),
    (
        r'weight .tofloat(+strict)',
        ValueError,
    ),
    (
        r'weight .tonum(+strict)',
        ValueError,
    ),
    (
        r'diabetes .tobool(+strict)',
        TypeError,
    ),
    ])
def test_strict_type_errors(code, error_type):
    with pytest.raises(error_type):
        _ = df.dk.qr(code).result



def test_strict_type_colref1():
    code = r"""
    a = @b +colref +date +strict
    """
    df_test = pd.DataFrame({
        'a': ['2020-01-01', '2020-01-02'],
        'b': ['2021-02-01', '2021-02-02'],
        })
    result = df_test.dk.qr(code).result
    vals = [
        pd.to_datetime('2021-02-01').date(),
        pd.to_datetime('2021-02-02').date(),
        ]
    expected = pd.DataFrame({'a': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_strict_type_colref2():
    code = r"""
    a = @b +colref +datetime +strict
    """
    df_test = pd.DataFrame({
        'a': ['2020-01-01 00:00:00', '2020-01-02 03:04:05'],
        'b': ['2021-02-01 01:02:03', '2021-02-02 04:05:06'],
        })
    result = df_test.dk.qr(code).result
    vals = [
        pd.to_datetime('2021-02-01 01:02:03'),
        pd.to_datetime('2021-02-02 04:05:06'),
        ]
    expected = pd.DataFrame({'a': vals}, dtype='datetime64[us]')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_typeinfo_cols():
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




def test_typeinfo_rows():
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




def test_typeinfo_vals():
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




def test_typeinfo_strict_cols():
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




def test_typeinfo_strict_rows():
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




def test_typeinfo_strict_vals():
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
