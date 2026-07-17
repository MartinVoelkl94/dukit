
import pandas as pd
import numpy as np
import pytest

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
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




def test_raw_rep():
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




params = [
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
    ]
@pytest.mark.parametrize('code, error_type', params)
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




def test_to_bool1():
    code = r"""
    name  .tobool()
    """
    result = df.dk.qr(code).result
    vals = [np.nan] * 11
    expected = pd.DataFrame({'name': vals}, dtype='boolean')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_bool2():
    code = r"""
    diabetes  .tobool()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='boolean')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_bool3():
    code = r"""
    diabetes  :isyn() .tobool()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_bool4():
    code = r"""
    diabetes  %%:isyn()  %%%.tobool()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_date1():
    code = r"""
    name  .todate()
    """
    result = df.dk.qr(code).result
    vals = [None] * 11
    expected = pd.DataFrame({'name': vals}, dtype='datetime64[s]')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_date2():
    code = r"""
    'date of birth'  .todate()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    vals = [pd.to_datetime(val).date() for val in vals]
    expected = pd.DataFrame({'date of birth': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_date3():
    code = r"""
    'date of birth'  %%!:isint() .todate()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'date of birth': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_datetime1():
    code = r"""
    name  .todatetime()
    """
    result = df.dk.qr(code).result
    vals = [None] * 11
    expected = pd.DataFrame({'name': vals}, dtype='datetime64[us]')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_datetime2():
    code = r"""
    'date of birth'  .todatetime()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    vals = [pd.to_datetime(val) for val in vals]
    expected = pd.DataFrame({'date of birth': vals}, dtype='datetime64[us]')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_datetime3():
    code = r"""
    'date of birth'  %%!:isint() .todatetime()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'date of birth': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_datetime4():
    code = r"""
    'date of birth'  %%!:isint() .todatetime()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'date of birth': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_float1():
    code = r"""
    name  .tofloat()
    """
    result = df.dk.qr(code).result
    vals = [np.nan] * 11
    expected = pd.DataFrame({'name': vals}, dtype='Float64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_float2():
    code = r"""
    weight .tofloat()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='Float64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_float3():
    code = r"""
    weight %%>70 .tofloat()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_float4():
    code = r"""
    weight  %%>70  %%%.tofloat()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals})
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_int1():
    code = r"""
    name  .toint()
    """
    result = df.dk.qr(code).result
    vals = [np.nan] * 11
    expected = pd.DataFrame({'name': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_int2():
    code = r"""
    name  %%%.toint()
    """
    result = df.dk.qr(code).result
    vals = [np.nan] * 11
    expected = pd.DataFrame({'name': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_int3():
    code = r"""
    weight .toint()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_int4():
    code = r"""
    weight %%>70 .toint()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_int5():
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




def test_to_na1():
    code = r"""
    name .tona()
    """
    result = df.dk.qr(code).result
    expected = get_df()[['name']]
    assert_frame_equal(result, expected)




def test_to_na2():
    code = r"""
    diabetes  .tona()
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_na3():
    code = r"""
    diabetes  %%!?'/'  .tona()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_na4():
    code = r"""
    diabetes  %%!?'/'  %%%.tona()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_nk1():
    code = r"""
    age  .tonk
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_nk2():
    code = r"""
    age  :!>0  .tonk  %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_num1():
    code = r"""
    name  .tonum()
    """
    result = df.dk.qr(code).result
    vals = pd.Series([pd.NA] * 11, dtype='Int64')
    expected = pd.DataFrame({'name': vals})
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_num2():
    code = r"""
    weight .tonum()
    """
    result = df.dk.qr(code).result
    vals = pd.Series([
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
        dtype='Float64',
        )
    expected = pd.DataFrame({'weight': vals})
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_num3():
    code = r"""
    weight %%>70 .tonum()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_num4():
    code = r"""
    weight  %%>70  %%%.tonum()
    %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'weight': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_to_obj():
    code = r"""
    age  .toobj
    """
    result = df.dk.qr(code).result
    expected = get_df()[['age']].astype('object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_yn1():
    code = r"""
    diabetes  .toyn
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_to_yn2():
    code = r"""
    diabetes  !=7 +index  .toyn  %%
    """
    result = df.dk.qr(code).result
    vals = [
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
        ]
    expected = pd.DataFrame({'diabetes': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_typeinfo():
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




def test_typeinfo_strict():
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
