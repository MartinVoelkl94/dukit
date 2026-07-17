
import pandas as pd
import pytest

from pandas.testing import assert_series_equal
from dukit.qlang import (
    engine,
    symbols,
    )
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




params = [
    (
        pd.Series(['A', 'b']),
        pd.Series(['a', 'b'], dtype='string'),
        'abc',
        'abc',
    ),
    (
        pd.Series([1.2, 2.8]),
        pd.Series([1.2, 2.8]),
        '1',
        1,
    ),
    (
        pd.Series([1.2, 2.8]),
        pd.Series([1.2, 2.8], dtype='Float64'),
        '1.5',
        1.5,
    ),
    (
        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),
        '1e0',
        1.0,
    ),
    (
        pd.Series(['yes', 'no']),
        pd.Series([True, False], dtype='boolean'),
        'true',
        True,
    ),
    (
        pd.Series([
            '2020-01-01',
            '2020-01-02',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01').date(),
            pd.to_datetime('2020-01-02').date(),
            ], dtype='object'),
        '2020-01-01',
        pd.to_datetime('2020-01-01').date(),
    ),
    (
        pd.Series([
            '2020-01-01 00:00:00',
            '2020-01-02 00:00:00',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01 00:00:00'),
            pd.to_datetime('2020-01-02 00:00:00'),
            ], dtype='datetime64[us]'),
        '2020-01-01 00:00:00',
        pd.to_datetime('2020-01-01 00:00:00'),
    ),
]
@pytest.mark.parametrize('series, series_expected, arg, arg_expected', params)
def test_infer_types_for_getter(series, series_expected, arg, arg_expected):
    op = engine.Symbol()
    query = df.dk.q()
    series_new, arg_new = symbols._infer_types_for_getter(series, arg, op, query)

    assert_series_equal(series_new, series_expected)
    assert arg_new == arg_expected




params = [
    (
        {'str': ''},
        pd.Series(['A', 'b']),
        pd.Series(['a', 'b'], dtype='string'),
        'C',
        'c',
    ),
    (
        {'int': ''},
        pd.Series([1.2, 2.8]),
        pd.Series([1, 3], dtype='Int64'),
        '2',
        2,
    ),
    (
        {'float': ''},
        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),
        '2.25',
        2.25,
    ),
    (
        {'num': ''},
        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),
        '1e0',
        1.0,
    ),
    (
        {'bool': ''},
        pd.Series(['yes', 'no']),
        pd.Series([True, False], dtype='boolean'),
        'true',
        True,
    ),
    (
        {'date': ''},
        pd.Series([
            '2020-01-01',
            '2020-01-02',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01').date(),
            pd.to_datetime('2020-01-02').date(),
            ], dtype='object'),
        '2020-01-03',
        pd.to_datetime('2020-01-03').date(),
    ),
    (
        {'datetime': ''},
        pd.Series([
            '2020-01-01 00:00:00',
            '2020-01-02 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01 00:00:00'),
            pd.to_datetime('2020-01-02 01:02:03'),
            ], dtype='datetime64[us]'),
        '2020-01-03 04:05:06',
        pd.to_datetime('2020-01-03 04:05:06'),
    ),
    (
        {'strict': '', 'str': ''},
        pd.Series(['A', 'b']),
        pd.Series(['A', 'b'], dtype='string'),
        'C',
        'C',
    ),
    (
        {'strict': '', 'int': ''},
        pd.Series([1, 2], dtype='Int64'),
        pd.Series([1, 2], dtype='Int64'),
        '3',
        3,
    ),
    (
        {'strict': '', 'float': ''},
        pd.Series([1.0, 2.0]),
        pd.Series([1.0, 2.0], dtype='Float64'),
        '3.5',
        3.5,
    ),
    (
        {'strict': '', 'num': ''},
        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),
        '3e0',
        3.0,
    ),
    (
        {'strict': '', 'bool': ''},
        pd.Series([True, False]),
        pd.Series([True, False], dtype='boolean'),
        'true',
        True,
    ),
    (
        {'strict': '', 'date': ''},
        pd.Series([
            '2020-01-01',
            '2020-01-02',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01').date(),
            pd.to_datetime('2020-01-02').date(),
            ], dtype='object'),
        '2020-01-03',
        pd.to_datetime('2020-01-03').date(),
    ),
    (
        {'strict': '', 'datetime': ''},
        pd.Series([
            '2020-01-01 00:00:00',
            '2020-01-02 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01 00:00:00'),
            pd.to_datetime('2020-01-02 01:02:03'),
            ], dtype='datetime64[us]'),
        '2020-01-03 00:00:00',
        pd.to_datetime('2020-01-03 00:00:00'),
    ),
    (
        {'strict': ''},
        pd.Series(['A', 'b']),
        pd.Series(['A', 'b']),
        'abc',
        'abc',
    ),
]
@pytest.mark.parametrize('flags, series, series_expected, arg, arg_expected', params)
def test_process_types(flags, series, series_expected, arg, arg_expected):
    op = engine.Symbol()
    op.flags = flags.copy()
    op.category = 'getter'
    query = df.dk.q()
    series_new, arg_new = symbols._process_types(series, arg, op, query)

    assert_series_equal(series_new, series_expected)
    assert arg_new == arg_expected




def test_process_types_default():
    op = engine.Symbol()
    op.category = 'setter'
    query = df.dk.q()
    series = pd.Series(['A', 'B'])

    series_new, arg_new = symbols._process_types(series, 'abc', op, query)

    assert_series_equal(series_new, series.astype('object'))
    assert arg_new == 'abc'




params = [
    (
        {'str': ''},

        pd.Series(['A', 'b']),
        pd.Series(['a', 'b'], dtype='string'),

        pd.Series(['C', 'D']),
        pd.Series(['c', 'd'], dtype='string'),
    ),
    (
        {'int': ''},

        pd.Series(['1.2', '2.8']),
        pd.Series([1, 3], dtype='Int64'),

        pd.Series(['3.4', '4.6']),
        pd.Series([3, 5], dtype='Int64'),
    ),
    (
        {'float': ''},

        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),

        pd.Series(['3', '4.5']),
        pd.Series([3.0, 4.5], dtype='Float64'),
    ),
    (
        {'num': ''},

        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),

        pd.Series(['3', '4.5']),
        pd.Series([3.0, 4.5], dtype='Float64'),
    ),
    (
        {'bool': ''},

        pd.Series(['yes', 'no']),
        pd.Series([True, False], dtype='boolean'),

        pd.Series(['true', 'false']),
        pd.Series([True, False], dtype='boolean'),
    ),
    (
        {'date': ''},

        pd.Series([
            '2020-01-01',
            '2020-01-02',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01').date(),
            pd.to_datetime('2020-01-02').date(),
            ], dtype='object'),

        pd.Series([
            '2020-01-03',
            '2020-01-04',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-03').date(),
            pd.to_datetime('2020-01-04').date(),
            ], dtype='object'),
    ),
    (
        {'datetime': ''},

        pd.Series([
            '2020-01-01 00:00:00',
            '2020-01-02 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01 00:00:00'),
            pd.to_datetime('2020-01-02 01:02:03'),
            ], dtype='datetime64[us]'),

        pd.Series([
            '2020-01-03 00:00:00',
            '2020-01-04 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-03 00:00:00'),
            pd.to_datetime('2020-01-04 01:02:03'),
            ], dtype='datetime64[us]'),
    ),
    (
        {'strict': '', 'int': ''},

        pd.Series([1, 2], dtype='Int64'),
        pd.Series([1, 2], dtype='Int64'),

        pd.Series(['3', '4']),
        pd.Series([3, 4], dtype='Int64'),
    ),
    (
        {'strict': '', 'str': ''},

        pd.Series(['A', 'b']),
        pd.Series(['A', 'b'], dtype='string'),

        pd.Series(['C', 'D']),
        pd.Series(['C', 'D'], dtype='string'),
    ),
    (
        {'strict': '', 'float': ''},

        pd.Series([1.0, 2.0]),
        pd.Series([1.0, 2.0], dtype='Float64'),

        pd.Series(['3.5', '4.5']),
        pd.Series([3.5, 4.5], dtype='Float64'),
    ),
    (
        {'strict': '', 'num': ''},

        pd.Series(['1', '2.5']),
        pd.Series([1.0, 2.5], dtype='Float64'),

        pd.Series(['3e0', '4e0']),
        pd.Series([3, 4], dtype='Int64'),
    ),
    (
        {'strict': '', 'bool': ''},
        pd.Series([True, False]),
        pd.Series([True, False], dtype='boolean'),

        pd.Series([True, False], dtype='boolean'),
        pd.Series([True, False], dtype='boolean'),
    ),
    (
        {'strict': '', 'date': ''},

        pd.Series([
            '2020-01-01',
            '2020-01-02',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01').date(),
            pd.to_datetime('2020-01-02').date(),
            ], dtype='object'),

        pd.Series([
            '2020-01-03',
            '2020-01-04',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-03').date(),
            pd.to_datetime('2020-01-04').date(),
            ], dtype='object'),
    ),
    (
        {'strict': '', 'datetime': ''},

        pd.Series([
            '2020-01-01 00:00:00',
            '2020-01-02 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-01 00:00:00'),
            pd.to_datetime('2020-01-02 01:02:03'),
            ], dtype='datetime64[us]'),

        pd.Series([
            '2020-01-03 00:00:00',
            '2020-01-04 01:02:03',
            ]),
        pd.Series([
            pd.to_datetime('2020-01-03 00:00:00'),
            pd.to_datetime('2020-01-04 01:02:03'),
            ], dtype='datetime64[us]'),
    ),
    (
        {'strict': ''},

        pd.Series(['A', 'b']),
        pd.Series(['A', 'b']),

        pd.Series(['abc', 'def']),
        pd.Series(['abc', 'def']),
    ),
    (
        {'strict': ''},

        pd.Series(['A', 'b'], dtype='string'),
        pd.Series(['A', 'b'], dtype='string'),

        pd.Series(['abc', 'def'], dtype='object'),
        pd.Series(['abc', 'def'], dtype='string'),
    ),
]
@pytest.mark.parametrize('flags, series1, series1_expected, series2, series2_expected', params)  # noqa: E501
def test_process_types_series(flags, series1, series1_expected, series2, series2_expected):  # noqa: E501
    query = df.dk.q()

    op = engine.Symbol()
    op.flags = flags.copy()
    series1_new, series2_new = symbols._process_types_series(
        series1,
        series2,
        op,
        query,
        )

    assert_series_equal(series1_new, series1_expected)
    assert_series_equal(series2_new, series2_expected)
