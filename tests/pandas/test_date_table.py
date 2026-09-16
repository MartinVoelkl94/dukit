
import datetime
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from dukit import date_table, log


def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error


def get_df():
    df = pd.DataFrame({
        'id': [
            'a',
            'b',
            'c',
            ],
        'date0': [
            '2026-01-25',
            '2026-02-03',
            None,
            ],
        'date1': [
            '2026-02-15',
            '2026-02-16',
            '2026-02-17',
            ],
        'date2': [
            '2026-02-20',
            '2026-02-25',
            '2026-02-26',
            ],
        'date3': [
            'nan',
            'na',
            np.nan,
            ],
        'date4': [
            pd.Timestamp('2026-03-05'),
            pd.NaT,
            pd.NA,
            ],
        'date5': [
            datetime.datetime(2026, 3, 5),
            pd.Timestamp('2026-03-10'),
            datetime.datetime(2026, 3, 8),
            ],
        })
    return df



def test_col():

    result = date_table(
        get_df(),
        reference_col='date1',
        )

    expected = pd.DataFrame()
    expected['days'] = [i for i in range(-21, 24) if i != 0]
    expected['0'] = ''
    expected['1'] = ''
    expected['2'] = ''

    expected.loc[expected['days'] == -21, '0'] = 'date0'
    expected.loc[expected['days'] == -13, '1'] = 'date0'

    expected.loc[expected['days'] == 1, '0'] = 'date1'
    expected.loc[expected['days'] == 1, '1'] = 'date1'
    expected.loc[expected['days'] == 1, '2'] = 'date1'

    expected.loc[expected['days'] == 6, '0'] = 'date2'
    expected.loc[expected['days'] == 10, '1'] = 'date2'
    expected.loc[expected['days'] == 10, '2'] = 'date2'

    expected.loc[expected['days'] == 19, '0'] = 'date4\ndate5\n'
    expected.loc[expected['days'] == 23, '1'] = 'date5'
    expected.loc[expected['days'] == 20, '2'] = 'date5'

    assert_frame_equal(result, expected)  #type: ignore



def test_uid():

    result = date_table(
        get_df(),
        reference_col='date1',
        uid='id',
        )

    expected = pd.DataFrame()
    expected['days'] = [i for i in range(-21, 24) if i != 0]
    expected['a'] = ''
    expected['b'] = ''
    expected['c'] = ''

    expected.loc[expected['days'] == -21, 'a'] = 'date0'
    expected.loc[expected['days'] == -13, 'b'] = 'date0'

    expected.loc[expected['days'] == 1, 'a'] = 'date1'
    expected.loc[expected['days'] == 1, 'b'] = 'date1'
    expected.loc[expected['days'] == 1, 'c'] = 'date1'

    expected.loc[expected['days'] == 6, 'a'] = 'date2'
    expected.loc[expected['days'] == 10, 'b'] = 'date2'
    expected.loc[expected['days'] == 10, 'c'] = 'date2'

    expected.loc[expected['days'] == 19, 'a'] = 'date4\ndate5\n'
    expected.loc[expected['days'] == 23, 'b'] = 'date5'
    expected.loc[expected['days'] == 20, 'c'] = 'date5'

    assert_frame_equal(result, expected)  #type: ignore



def test_upper_lower():

    result = date_table(
        get_df(),
        reference_col='date1',
        upper=20,
        lower=-20
        )

    expected = pd.DataFrame()
    expected['days'] = [i for i in range(-20, 21) if i != 0]
    expected['0'] = ''
    expected['1'] = ''
    expected['2'] = ''

    expected.loc[expected['days'] == -13, '1'] = 'date0'

    expected.loc[expected['days'] == 1, '0'] = 'date1'
    expected.loc[expected['days'] == 1, '1'] = 'date1'
    expected.loc[expected['days'] == 1, '2'] = 'date1'

    expected.loc[expected['days'] == 6, '0'] = 'date2'
    expected.loc[expected['days'] == 10, '1'] = 'date2'
    expected.loc[expected['days'] == 10, '2'] = 'date2'

    expected.loc[expected['days'] == 19, '0'] = 'date4\ndate5\n'
    expected.loc[expected['days'] == 20, '2'] = 'date5'

    assert_frame_equal(result, expected)  #type: ignore



def test_day0():

    result = date_table(
        get_df(),
        reference_col='date1',
        start_at_day1=False,
        )

    expected = pd.DataFrame()
    expected['days'] = [i for i in range(-21, 23)]
    expected['0'] = ''
    expected['1'] = ''
    expected['2'] = ''

    expected.loc[expected['days'] == -21, '0'] = 'date0'
    expected.loc[expected['days'] == -13, '1'] = 'date0'

    expected.loc[expected['days'] == 0, '0'] = 'date1'
    expected.loc[expected['days'] == 0, '1'] = 'date1'
    expected.loc[expected['days'] == 0, '2'] = 'date1'

    expected.loc[expected['days'] == 5, '0'] = 'date2'
    expected.loc[expected['days'] == 9, '1'] = 'date2'
    expected.loc[expected['days'] == 9, '2'] = 'date2'

    expected.loc[expected['days'] == 18, '0'] = 'date4\ndate5\n'
    expected.loc[expected['days'] == 22, '1'] = 'date5'
    expected.loc[expected['days'] == 19, '2'] = 'date5'

    assert_frame_equal(result, expected)  #type: ignore



def test_schedule():

    schedule = {
        -21: 'screening start',
        -1: 'screening end',
        1: 'visit 1',
        8: 'visit 2',
        15: 'visit 3',
        22: 'visit 4',
        29: 'visit 5',
        }

    result = date_table(
        get_df(),
        reference_col='date1',
        schedule=schedule,
        )

    expected = pd.DataFrame()
    expected['days'] = [i for i in range(-21, 24) if i != 0]
    expected['planned'] = ''
    expected['0'] = ''
    expected['1'] = ''
    expected['2'] = ''

    expected.loc[expected['days'] == -21, 'planned'] = 'screening start'
    expected.loc[expected['days'] == -1, 'planned'] = 'screening end'
    expected.loc[expected['days'] == 1, 'planned'] = 'visit 1'
    expected.loc[expected['days'] == 8, 'planned'] = 'visit 2'
    expected.loc[expected['days'] == 15, 'planned'] = 'visit 3'
    expected.loc[expected['days'] == 22, 'planned'] = 'visit 4'
    expected.loc[expected['days'] == 29, 'planned'] = 'visit 5'

    expected.loc[expected['days'] == -21, '0'] = 'date0'
    expected.loc[expected['days'] == -13, '1'] = 'date0'

    expected.loc[expected['days'] == 1, '0'] = 'date1'
    expected.loc[expected['days'] == 1, '1'] = 'date1'
    expected.loc[expected['days'] == 1, '2'] = 'date1'

    expected.loc[expected['days'] == 6, '0'] = 'date2'
    expected.loc[expected['days'] == 10, '1'] = 'date2'
    expected.loc[expected['days'] == 10, '2'] = 'date2'

    expected.loc[expected['days'] == 19, '0'] = 'date4\ndate5\n'
    expected.loc[expected['days'] == 23, '1'] = 'date5'
    expected.loc[expected['days'] == 20, '2'] = 'date5'

    assert_frame_equal(result.data, expected)  #type: ignore
