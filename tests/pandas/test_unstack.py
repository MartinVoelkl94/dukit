
import pandas as pd
import dukit as dk

from pandas.testing import assert_frame_equal
from dukit import get_df_medications1, get_df_medications3



def test_unstack():

    medications = get_df_medications1()
    result = medications.dk.unstack(
        'id',
        uid_pattern = r'(?P<uid>.+)_(?P<subid>.+)',
        col_template = '{col}_{subid}',
        cols_keep = None,
        stagger = True,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications3()

    assert_frame_equal(result, expected)



def test_unstack_default():

    medications = get_df_medications1()
    result = medications.dk.unstack(
        'id',
        ).convert_dtypes()

    expected = get_df_medications3()

    assert_frame_equal(result, expected)



def test_unstack_unstaggered():

    medications = get_df_medications1()
    result = medications.dk.unstack(
        'id',
        uid_pattern = r'(?P<uid>.+)_(?P<subid>.+)',
        col_template = '{col}_{subid}',
        cols_keep = None,
        stagger = False,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications3()
    cols_reordered = [
        'id',
        'medication_1',
        'medication_2',
        'medication_3',
        'dose_1',
        'dose_2',
        'dose_3',
        'unit_1',
        'unit_2',
        'unit_3',
        ]
    expected = expected[cols_reordered]

    assert_frame_equal(result, expected)



def test_unstack_template():

    medications = get_df_medications1()
    result = medications.dk.unstack(
        'id',
        uid_pattern = r'(?P<uid>.+)_(?P<subid>.+)',
        col_template = '#{subid}_{col}',
        cols_keep = None,
        stagger = True,
        verbosity = 3
        ).convert_dtypes()

    temp = get_df_medications3()
    expected = temp[['id']]

    for col in temp.columns:
        if col == 'id':
            continue
        counter = col.split('_')[1]
        colname = col.split('_')[0]
        expected[f'#{counter}_{colname}'] = temp[col]

    assert_frame_equal(result, expected)
