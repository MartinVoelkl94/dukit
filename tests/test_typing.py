
import pytest
import datetime
import numpy as np
import pandas as pd
import dukit as dk

from faker import Faker


custom_types = [
    dk.int,
    dk.float,
    dk.num,
    dk.bool,
    dk.date,
    dk.datetime,
    dk.na,
    dk.nk,
    dk.yn,
    ]



@pytest.mark.parametrize('input, expected', [
    ('y', True),
    ('yes', True),
    ('true', True),
    ('1', True),
    ('1.0', True),
    ('positive', True),
    ('pos', True),

    ('n', False),
    ('no', False),
    ('false', False),
    ('0', False),
    ('0.0', False),
    ('negative', False),
    ('neg', False),

    ('Y', True),
    ('YES', True),
    ('TRUE', True),
    ('1', True),
    ('1.0', True),
    ('POSITIVE', True),
    ('POS', True),

    ('N', False),
    ('NO', False),
    ('FALSE', False),
    ('0', False),
    ('0.0', False),
    ('NEGATIVE', False),
    ('NEG', False),

    (0, False),
    (0.0, False),
    (1, True),
    (1.0, True),
    ])
def test_bool(input, expected):
    result = dk.bool(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    (1, 1),
    (np.int8(1), 1),
    (np.int16(1), 1),
    (np.int32(1), 1),
    (np.int64(1), 1),

    (1.0, 1.0),
    (np.float16(1.0), 1.0),
    (np.float32(1.0), 1.0),
    (np.float64(1.0), 1.0),

    (True, True),
    (False, False),

    ('1', 1),
    ('1.0', 1.0),
    ('1.5', 1.5),
    ('True', True),
    ('yes', 'yes'),
    ('text', 'text'),
    ('20240411', 20240411),

    (None, None),
    ('123abc', '123abc'),
    ('TrueFalse', 'TrueFalse'),
    ('2024-13-32', '2024-13-32'),
    (complex(1, 1), complex(1, 1)),

    ('2024-04-11', datetime.datetime(2024, 4, 11).date()),
    ('2024.04.11', datetime.datetime(2024, 4, 11).date()),
    ('2024/04/11', datetime.datetime(2024, 4, 11).date()),
    ('2024_04_11', datetime.datetime(2024, 4, 11).date()),
    ('2024\\04\\11', datetime.datetime(2024, 4, 11).date()),

    ('11-04-2024', datetime.datetime(2024, 4, 11).date()),
    ('11.04.2024', datetime.datetime(2024, 4, 11).date()),
    ('11/04/2024', datetime.datetime(2024, 4, 11).date()),
    ('11_04_2024', datetime.datetime(2024, 4, 11).date()),
    ('11\\04\\2024', datetime.datetime(2024, 4, 11).date()),

    ('Apr112024', datetime.datetime(2024, 4, 11).date()),
    ('11Apr2024', datetime.datetime(2024, 4, 11).date()),
    ('2024Apr11', datetime.datetime(2024, 4, 11).date()),
    ('Apr-11-2024', datetime.datetime(2024, 4, 11).date()),
    ('Apr-11-2024', datetime.datetime(2024, 4, 11).date()),
    ('Apr.11.2024', datetime.datetime(2024, 4, 11).date()),
    ('Apr/11/2024', datetime.datetime(2024, 4, 11).date()),
    ('Apr_11_2024', datetime.datetime(2024, 4, 11).date()),
    ('Apr\\11\\2024', datetime.datetime(2024, 4, 11).date()),


    ('November112024', datetime.datetime(2024, 11, 11).date()),
    ('11November2024', datetime.datetime(2024, 11, 11).date()),
    ('2024November11', datetime.datetime(2024, 11, 11).date()),
    ('November-11-2024', datetime.datetime(2024, 11, 11).date()),
    ('November.11.2024', datetime.datetime(2024, 11, 11).date()),
    ('November/11/2024', datetime.datetime(2024, 11, 11).date()),
    ('November_11_2024', datetime.datetime(2024, 11, 11).date()),
    ('November\\11\\2024', datetime.datetime(2024, 11, 11).date()),

    ('20240411 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024-04-11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11-04-2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr-11-2024 00:00:00', datetime.datetime(2024, 4, 11)),

    ('2024-04-11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024.04.11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024/04/11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024_04_11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024\\04\\11 00:00:00', datetime.datetime(2024, 4, 11)),

    ('11-04-2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11.04.2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11/04/2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11_04_2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11\\04\\2024 00:00:00', datetime.datetime(2024, 4, 11)),

    ('Apr-11-2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr-11-2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr.11.2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr/11/2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr_11_2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr112024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('11Apr2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ('2024Apr11 00:00:00', datetime.datetime(2024, 4, 11)),
    ('Apr\\11\\2024 00:00:00', datetime.datetime(2024, 4, 11)),
    ])
def test_convert(input, expected):
    result = dk.convert(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    ('2020-01-01', (2020, 1, 1)),
    ('2020-01-01 00:00:00', (2020, 1, 1)),

    ('2020-01-01', (2020, 1, 1)),
    ('2020.01.01', (2020, 1, 1)),
    ('2020/01/01', (2020, 1, 1)),
    ('2020\\01\\01', (2020, 1, 1)),
    ('2020_01_01', (2020, 1, 1)),
    ('2020 01 01', (2020, 1, 1)),
    ('20200101', (2020, 1, 1)),
    (20200101, (2020, 1, 1)),

    ('2020 Jan 01', (2020, 1, 1)),
    ('2020 January 01', (2020, 1, 1)),
    ('2020 Jan 1', (2020, 1, 1)),
    ('2020 January 1', (2020, 1, 1)),

    ('Jan 01 2020', (2020, 1, 1)),
    ('January 01 2020', (2020, 1, 1)),
    ('Jan 1 2020', (2020, 1, 1)),
    ('January 1 2020', (2020, 1, 1)),

    ('01 Jan 2020', (2020, 1, 1)),
    ('01 January 2020', (2020, 1, 1)),
    ('1 Jan 2020', (2020, 1, 1)),
    ('1 January 2020', (2020, 1, 1)),

    ('01-01-2020', (2020, 1, 1)),
    ('01.01.2020', (2020, 1, 1)),
    ('01/01/2020', (2020, 1, 1)),
    ('01 01 2020', (2020, 1, 1)),

    ('02-01-20', (2020, 1, 2)),
    ('02.01.20', (2020, 1, 2)),
    ('02/01/20', (2020, 1, 2)),
    ('02 01 20', (2020, 1, 2)),

    ('2020-01-02', (2020, 1, 2)),
    ('2020.01.02', (2020, 1, 2)),
    ('2020/01/02', (2020, 1, 2)),
    ('2020 01 02', (2020, 1, 2)),
    ('20200102', (2020, 1, 2)),

    ('2020-12-32', pd.NaT),
    ('2020.12.32', pd.NaT),
    ('2020/12/32', pd.NaT),
    ('2020\\12\\32', pd.NaT),
    ('2020_12_32', pd.NaT),
    ('2020 12 32', pd.NaT),
    ('20201232', pd.NaT),
    (20201232, pd.NaT),

    ('2020-13-30', pd.NaT),
    ('2020.13.30', pd.NaT),
    ('2020/13/30', pd.NaT),
    ('2020\\13\\30', pd.NaT),
    ('2020_13_30', pd.NaT),
    ('2020 13 30', pd.NaT),
    ('20201330', pd.NaT),
    (20201330, pd.NaT),

    ])
def test_date(input, expected):
    result = dk.date(input)
    if expected is pd.NaT:
        text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
        assert result is expected, text
    else:
        expected = datetime.date(*expected)
        text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
        assert result == expected, text



def test_date_random():
    Faker.seed(1)
    fake = Faker()

    for i in range(1000):
        date_str = fake.date()
        result = dk.date(date_str)
        expected = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        assert result == expected, f'Expected {expected}, but got {result}'


@pytest.mark.parametrize('input, expected', [
    (0, pd.NaT),

    ('2020-02-01', (2020, 2, 1)),
    ('20200201', (2020, 2, 1)),
    ('2020-02-01 00:00:00', (2020, 2, 1)),
    ('2020-02-01 00:00:01', (2020, 2, 1, 0, 0, 1)),
    ('2020-02-01 00:01:00', (2020, 2, 1, 0, 1, 0)),
    ('2020-02-01 01:00:00', (2020, 2, 1, 1, 0, 0)),
    ('2020-02-01 01:01:01', (2020, 2, 1, 1, 1, 1)),
    ('20200201 01:01:01', (2020, 2, 1, 1, 1, 1)),

    ('2020.02.01', (2020, 2, 1)),
    ('2020/02/01', (2020, 2, 1)),
    ('2020 02 01', (2020, 2, 1)),

    ('2020 Feb 01', (2020, 2, 1)),
    ('2020 February 01', (2020, 2, 1)),
    ('2020 Feb 1', (2020, 2, 1)),
    ('2020 February 1', (2020, 2, 1)),


    ('Feb 01 2020', (2020, 2, 1)),
    ('February 01 2020', (2020, 2, 1)),
    ('Feb 1 2020', (2020, 2, 1)),
    ('February 1 2020', (2020, 2, 1)),

    ('01 Feb 2020', (2020, 2, 1)),
    ('01 February 2020', (2020, 2, 1)),
    ('1 Feb 2020', (2020, 2, 1)),
    ('1 February 2020', (2020, 2, 1)),

    ('01-02-2020', (2020, 2, 1)),
    ('01.02.2020', (2020, 2, 1)),
    ('01/02/2020', (2020, 2, 1)),

    ('01-02-20', (2020, 2, 1)),
    ('01.02.20', (2020, 2, 1)),
    ('01/02/20', (2020, 2, 1)),
    ('01 02 20', (2020, 2, 1)),

    ('2020-02-01', (2020, 2, 1)),
    ('2020.02.01', (2020, 2, 1)),
    ('2020/02/01', (2020, 2, 1)),
    ('2020 02 01', (2020, 2, 1)),
    ])
def test_datetime(input, expected):
    result = dk.datetime(input)
    if expected is pd.NaT:
        text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
        assert result is expected, text
    else:
        expected = datetime.datetime(*expected)
        text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
        assert result == expected, text


def test_datetime_random():
    Faker.seed(1)
    fake = Faker()

    for i in range(1000):
        date_str = fake.date_time().strftime('%Y-%m-%d %H:%M:%S')
        result = dk.datetime(date_str)
        expected = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        assert result == expected, f'Expected {expected}, but got {result}'



def test_errors_raise():
    for func in custom_types:
        with pytest.raises(ValueError):
            func('abc', errors='raise')


def test_errors_ignore():
    for func in custom_types:
        assert func('abc', errors='ignore') == 'abc'


def test_errors_coerce():
    assert dk.int('abc', errors='coerce') is np.nan
    assert dk.float('abc', errors='coerce') is np.nan
    assert dk.num('abc', errors='coerce') is np.nan
    assert dk.date('abc', errors='coerce') is pd.NaT
    assert dk.datetime('abc', errors='coerce') is pd.NaT
    assert dk.bool('abc', errors='coerce') is None
    assert dk.na('abc', errors='coerce') is None
    assert dk.nk('abc', errors='coerce') is None
    assert dk.yn('abc', errors='coerce') is None


def test_errors_custom():
    for func in custom_types:
        assert func('abc', errors='coerce', na=None) is None
        assert func('abc', errors='custom') == 'custom'



@pytest.mark.parametrize('func, value, errors, na, expected', [
    (dk.int, 'abc', 'ignore', np.nan, 'abc'),
    (dk.int, 'abc', 'coerce', -1, -1),
    (dk.int, 'abc', 'fallback', np.nan, 'fallback'),
    (dk.float, 'abc', 'ignore', np.nan, 'abc'),
    (dk.float, 'abc', 'coerce', -1.0, -1.0),
    (dk.num, 'abc', 'ignore', np.nan, 'abc'),
    (dk.num, 'abc', 'coerce', -1.0, -1.0),
    (dk.bool, 'maybe', 'ignore', None, 'maybe'),
    (dk.bool, 'maybe', 'coerce', None, None),
    (dk.bool, 'maybe', 'fallback', None, 'fallback'),
    (dk.na, 'text', 'ignore', None, 'text'),
    (dk.na, 'text', 'coerce', None, None),
    (dk.nk, 'text', 'ignore', 'unknown', 'text'),
    (dk.nk, 'text', 'coerce', 'unknown', 'unknown'),
    (dk.yn, 'text', 'ignore', None, 'text'),
    (dk.yn, 'text', 'coerce', None, None),
    ])
def test_fallbacks(func, value, errors, na, expected):
    result = func(value, errors=errors, na=na)
    if pd.isna(expected):
        assert pd.isna(result)
    else:
        assert result == expected



@pytest.mark.parametrize('input, expected', [
    ('1', 1.0),
    ('1.0', 1.0),
    ('1.1', 1.1),

    ('0', 0.0),
    ('0.0', 0.0),
    ('0.1', 0.1),

    ('-1', -1.0),
    ('-1.0', -1.0),
    ('-1.1', -1.1),

    (1, 1.0),
    (1.0, 1.0),
    (1.1, 1.1),

    (0, 0.0),
    (0.0, 0.0),
    (0.1, 0.1),

    (-1, -1.0),
    (-1.0, -1.0),
    (-1.1, -1.1),

    ('1e0', 1.0),
    ('1_000', 1000.0),
    ])
def test_float(input, expected):
    result = dk.float(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    ('1', 1),
    ('1.0', 1),
    ('1.1', 1),
    ('1.9', 2),
    ('1.5', 2),

    ('0', 0),
    ('0.0', 0),
    ('0.1', 0),
    ('0.9', 1),
    ('0.5', 0),

    ('-1', -1),
    ('-1.0', -1),
    ('-1.1', -1),
    ('-1.9', -2),
    ('-1.5', -2),

    (1, 1),
    (1.0, 1),
    (1.1, 1),
    (1.9, 2),
    (1.5, 2),

    (0, 0),
    (0.0, 0),
    (0.1, 0),
    (0.9, 1),
    (0.5, 0),

    (-1, -1),
    (-1.0, -1),
    (-1.1, -1),
    (-1.9, -2),
    (-1.5, -2),

    ('1e0', 1),
    ('1_000', 1000),

    (True, np.nan),
    (False, np.nan),
    ])
def test_int(input, expected):
    result = dk.int(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    if input is True or input is False:
        assert result is expected, text
    else:
        assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    ('1', 1),
    ('1.0', 1.0),
    ('1.1', 1.1),

    ('0', 0),
    ('0.0', 0.0),
    ('0.1', 0.1),

    ('-1', -1),
    ('-1.0', -1.0),
    ('-1.1', -1.1),

    (1, 1),
    (1.0, 1.0),
    (1.1, 1.1),

    (0, 0),
    (0.0, 0.0),
    (0.1, 0.1),

    (-1, -1),
    (-1.0, -1.0),
    (-1.1, -1.1),

    ('1e0', 1),
    ])
def test_num(input, expected):
    result = dk.num(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    (None, None),
    (np.nan, None),
    (pd.NaT, None),
    (pd.NA, None),
    ('', None),
    (' ', None),
    ('nan', None),
    ('NaN', None),
    ('NAN', None),
    ('na', None),
    ('NA', None),
    ('n/a', None),
    ('N/A', None),
    ('none', None),
    ('None', None),
    ('NONE', None),
    ('null', None),
    ('Null', None),
    ('NULL', None),
    ('nil', None),
    ('Nil', None),
    ('NIL', None),
    ('missing', None),
    ('Missing', None),
    ('MISSING', None),
    ('not available', None),
    ('Not available', None),
    ('NOT AVAILABLE', None),
    ('not a number', None),
    ('Not a number', None),
    ('NOT A NUMBER', None),
    ('not applicable', None),
    ('Not applicable', None),
    ('NOT APPLICABLE', None),
    ('not applicable', None),
    ('Not applicable', None),
    ('NOT APPLICABLE', None),
    ('not applicable', None),
    ('Not applicable', None),
    ('NOT APPLICABLE', None),
    ('void', None),
    ('Void', None),
    ('VOID', None),
    ('empty', None),
    ('Empty', None),
    ('EMPTY', None),
    ('blank', None),
    ('Blank', None),
    ('BLANK', None),
    ])
def test_na(input, expected):
    result = dk.na(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text


@pytest.mark.parametrize('input, expected', [
    ('unk', 'unknown'),
    ('unknown', 'unknown'),
    ('not known', 'unknown'),
    ('not known.', 'unknown'),
    ('nk', 'unknown'),
    ('n.k.', 'unknown'),
    ('n.k', 'unknown'),
    ('n/k', 'unknown'),
    ('not specified', 'unknown'),
    ('not specified.', 'unknown'),
    ('not specified', 'unknown'),
    ('not specified.', 'unknown'),
    ])
def test_nk(input, expected):
    result = dk.nk(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [

    (1, 'int'),
    (-1, 'int'),
    (np.int8(1), 'int'),
    (np.int16(1), 'int'),
    (np.int32(1), 'int'),
    (np.int64(1), 'int'),

    (1.0, 'float'),
    (-1.0, 'float'),
    (np.float16(1.0), 'float'),
    (np.float32(1.0), 'float'),
    (np.float64(1.0), 'float'),

    (True, 'bool'),
    (False, 'bool'),

    ('1', 'int'),
    ('1.0', 'float'),
    ('-1.0', 'float'),
    ('-1.1', 'float'),
    ('1.5', 'float'),
    ('True', 'bool'),
    ('text', 'str'),
    ('00:00', 'str'),
    ('20240411', 'int'),
    ('2024_04_11', 'date'),

    (np.nan, 'float'),
    (None, 'na'),
    (pd.NA, 'na'),
    ('', 'na'),
    ('na', 'na'),
    ('<na>', 'na'),
    ('<n/a>', 'na'),
    ('n/a', 'na'),
    ('n.a', 'na'),
    ('n.a.', 'na'),
    ('na.', 'na'),
    ('n.a', 'na'),
    ('nan', 'na'),
    ('n.a.n', 'na'),
    ('n.a.n.', 'na'),
    ('not available', 'na'),
    ('not applicable', 'na'),
    ('not a number', 'na'),
    ('missing', 'na'),
    ('missing.', 'na'),
    ('null', 'na'),
    ('nil', 'na'),
    ('none', 'na'),
    ('void', 'na'),
    ('blank', 'na'),
    ('empty', 'na'),

    (complex(1, 1), 'complex'),
    (object(), 'object'),
    ('123abc', 'str'),
    ('2024-13-32', 'str'),
    ('TrueFalse', 'str'),

    (datetime.date(2020, 1, 1), 'date'),
    ('2024-04-11', 'date'),
    ('2024.04.11', 'date'),
    ('2024/04/11', 'date'),
    ('2024\\04\\11', 'date'),
    ('2024_04_11', 'date'),

    ('11-04-2024', 'date'),
    ('11.04.2024', 'date'),
    ('11/04/2024', 'date'),
    ('11\\04\\2024', 'date'),
    ('11_04_2024', 'date'),

    ('Apr-11-2024', 'date'),
    ('Apr-11-2024', 'date'),
    ('Apr.11.2024', 'date'),
    ('Apr/11/2024', 'date'),
    ('Apr\\11\\2024', 'date'),
    ('Apr_11_2024', 'date'),
    ('Apr112024', 'date'),
    ('11Apr2024', 'date'),
    ('2024Apr11', 'date'),

    ('November-11-2024', 'date'),
    ('November.11.2024', 'date'),
    ('November/11/2024', 'date'),
    ('November\\11\\2024', 'date'),
    ('November_11_2024', 'date'),
    ('November112024', 'date'),
    ('11November2024', 'date'),
    ('2024November11', 'date'),

    ('20240411 00:00:00', 'datetime'),
    ('2024-04-11 00:00:00', 'datetime'),
    ('2024-04-11 00:00:00', 'datetime'),
    ('11-04-2024 00:00:00', 'datetime'),
    ('Apr-11-2024 00:00:00', 'datetime'),

    ('2024-04-11 00:00:00', 'datetime'),
    ('2024.04.11 00:00:00', 'datetime'),
    ('2024/04/11 00:00:00', 'datetime'),
    ('2024\\04\\11 00:00:00', 'datetime'),
    ('2024_04_11 00:00:00', 'datetime'),

    ('11-04-2024 00:00:00', 'datetime'),
    ('11.04.2024 00:00:00', 'datetime'),
    ('11/04/2024 00:00:00', 'datetime'),
    ('11\\04\\2024 00:00:00', 'datetime'),
    ('11_04_2024 00:00:00', 'datetime'),

    ('Apr-11-2024 00:00:00', 'datetime'),
    ('Apr-11-2024 00:00:00', 'datetime'),
    ('Apr.11.2024 00:00:00', 'datetime'),
    ('Apr/11/2024 00:00:00', 'datetime'),
    ('Apr\\11\\2024 00:00:00', 'datetime'),
    ('Apr_11_2024 00:00:00', 'datetime'),
    ('Apr112024 00:00:00', 'datetime'),
    ('11Apr2024 00:00:00', 'datetime'),
    ('2024Apr11 00:00:00', 'datetime'),

    ('November-11-2024 00:00:00', 'datetime'),
    ('November.11.2024 00:00:00', 'datetime'),
    ('November/11/2024 00:00:00', 'datetime'),
    ('November\\11\\2024 00:00:00', 'datetime'),
    ('November_11_2024 00:00:00', 'datetime'),
    ('November112024 00:00:00', 'datetime'),
    ('11November2024 00:00:00', 'datetime'),
    ('2024November11 00:00:00', 'datetime'),
    ])
def test_type(input, expected):
    result = dk.type(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [

    (1, 'Int64'),
    (-1, 'Int64'),
    (np.int8(1), 'Int64'),
    (np.int16(1), 'Int64'),
    (np.int32(1), 'Int64'),
    (np.int64(1), 'Int64'),

    (1.0, 'Float64'),
    (-1.0, 'Float64'),
    (np.float16(1.0), 'Float64'),
    (np.float32(1.0), 'Float64'),
    (np.float64(1.0), 'Float64'),

    (True, 'boolean'),
    (False, 'boolean'),

    ('1', 'Int64'),
    ('1.0', 'Float64'),
    ('-1.0', 'Float64'),
    ('-1.1', 'Float64'),
    ('1.5', 'Float64'),
    ('True', 'boolean'),
    ('text', 'string'),
    ('00:00', 'string'),
    ('20240411', 'Int64'),
    ('2024_04_11', 'datetime64[us]'),

    (np.nan, 'Float64'),
    (None, 'object'),
    (pd.NA, 'object'),
    ('', 'object'),
    ('na', 'object'),
    ('<na>', 'object'),
    ('<n/a>', 'object'),
    ('n/a', 'object'),
    ('n.a', 'object'),
    ('n.a.', 'object'),
    ('na.', 'object'),
    ('n.a', 'object'),
    ('nan', 'object'),
    ('n.a.n', 'object'),
    ('n.a.n.', 'object'),
    ('not available', 'object'),
    ('not applicable', 'object'),
    ('not a number', 'object'),
    ('missing', 'object'),
    ('missing.', 'object'),
    ('null', 'object'),
    ('nil', 'object'),
    ('none', 'object'),
    ('void', 'object'),
    ('blank', 'object'),
    ('empty', 'object'),

    (complex(1, 1), 'object'),
    (object(), 'object'),
    ('123abc', 'string'),
    ('2024-13-32', 'string'),
    ('TrueFalse', 'string'),

    (datetime.date(2020, 1, 1), 'datetime64[us]'),
    ('2024-04-11', 'datetime64[us]'),
    ('2024.04.11', 'datetime64[us]'),
    ('2024/04/11', 'datetime64[us]'),
    ('2024\\04\\11', 'datetime64[us]'),
    ('2024_04_11', 'datetime64[us]'),

    ('11-04-2024', 'datetime64[us]'),
    ('11.04.2024', 'datetime64[us]'),
    ('11/04/2024', 'datetime64[us]'),
    ('11\\04\\2024', 'datetime64[us]'),
    ('11_04_2024', 'datetime64[us]'),

    ('Apr-11-2024', 'datetime64[us]'),
    ('Apr-11-2024', 'datetime64[us]'),
    ('Apr.11.2024', 'datetime64[us]'),
    ('Apr/11/2024', 'datetime64[us]'),
    ('Apr\\11\\2024', 'datetime64[us]'),
    ('Apr_11_2024', 'datetime64[us]'),
    ('Apr112024', 'datetime64[us]'),
    ('11Apr2024', 'datetime64[us]'),
    ('2024Apr11', 'datetime64[us]'),

    ('November-11-2024', 'datetime64[us]'),
    ('November.11.2024', 'datetime64[us]'),
    ('November/11/2024', 'datetime64[us]'),
    ('November\\11\\2024', 'datetime64[us]'),
    ('November_11_2024', 'datetime64[us]'),
    ('November112024', 'datetime64[us]'),
    ('11November2024', 'datetime64[us]'),
    ('2024November11', 'datetime64[us]'),

    ('20240411 00:00:00', 'datetime64[us]'),
    ('2024-04-11 00:00:00', 'datetime64[us]'),
    ('2024-04-11 00:00:00', 'datetime64[us]'),
    ('11-04-2024 00:00:00', 'datetime64[us]'),
    ('Apr-11-2024 00:00:00', 'datetime64[us]'),

    ('2024-04-11 00:00:00', 'datetime64[us]'),
    ('2024.04.11 00:00:00', 'datetime64[us]'),
    ('2024/04/11 00:00:00', 'datetime64[us]'),
    ('2024\\04\\11 00:00:00', 'datetime64[us]'),
    ('2024_04_11 00:00:00', 'datetime64[us]'),

    ('11-04-2024 00:00:00', 'datetime64[us]'),
    ('11.04.2024 00:00:00', 'datetime64[us]'),
    ('11/04/2024 00:00:00', 'datetime64[us]'),
    ('11\\04\\2024 00:00:00', 'datetime64[us]'),
    ('11_04_2024 00:00:00', 'datetime64[us]'),

    ('Apr-11-2024 00:00:00', 'datetime64[us]'),
    ('Apr-11-2024 00:00:00', 'datetime64[us]'),
    ('Apr.11.2024 00:00:00', 'datetime64[us]'),
    ('Apr/11/2024 00:00:00', 'datetime64[us]'),
    ('Apr\\11\\2024 00:00:00', 'datetime64[us]'),
    ('Apr_11_2024 00:00:00', 'datetime64[us]'),
    ('Apr112024 00:00:00', 'datetime64[us]'),
    ('11Apr2024 00:00:00', 'datetime64[us]'),
    ('2024Apr11 00:00:00', 'datetime64[us]'),

    ('November-11-2024 00:00:00', 'datetime64[us]'),
    ('November.11.2024 00:00:00', 'datetime64[us]'),
    ('November/11/2024 00:00:00', 'datetime64[us]'),
    ('November\\11\\2024 00:00:00', 'datetime64[us]'),
    ('November_11_2024 00:00:00', 'datetime64[us]'),
    ('November112024 00:00:00', 'datetime64[us]'),
    ('11November2024 00:00:00', 'datetime64[us]'),
    ('2024November11 00:00:00', 'datetime64[us]'),
    ])
def test_dtype(input, expected):
    result = dk.dtype(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text



@pytest.mark.parametrize('input, expected', [
    ('y', 'yes'),
    ('yes', 'yes'),
    ('true', 'yes'),
    ('1', 'yes'),
    ('1.0', 'yes'),
    ('positive', 'yes'),
    ('pos', 'yes'),

    ('n', 'no'),
    ('no', 'no'),
    ('false', 'no'),
    ('0', 'no'),
    ('0.0', 'no'),
    ('negative', 'no'),
    ('neg', 'no'),

    ('Y', 'yes'),
    ('YES', 'yes'),
    ('TRUE', 'yes'),
    ('1', 'yes'),
    ('1.0', 'yes'),
    ('POSITIVE', 'yes'),
    ('POS', 'yes'),

    ('N', 'no'),
    ('NO', 'no'),
    ('FALSE', 'no'),
    ('0', 'no'),
    ('0.0', 'no'),
    ('NEGATIVE', 'no'),
    ('NEG', 'no'),

    (0, 'no'),
    (0.0, 'no'),
    (1, 'yes'),
    (1.0, 'yes'),
    ])
def test_yn(input, expected):
    result = dk.yn(input)
    text = f'\ninput: {input}\nRESULT: {result}\nEXPECTED: {expected}'
    assert result == expected, text
