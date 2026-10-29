
import pandas as pd
import dukit as dk

from pandas.testing import assert_frame_equal
from dukit import (
    log,
    get_df_medications1,
    get_df_medications2,
    get_df_medications3,
    )



def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



def test_stack():

    medications = get_df_medications3()
    result = medications.dk.stack(
        'id',
        col_pattern = r'(?P<col>.+)_(?P<subid>.+)',
        uid_template = '{uid}_{subid}',
        cols_keep = None,
        dropna = True,
        sort = True,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications2()

    assert_frame_equal(result, expected)



def test_stack_default():

    medications = get_df_medications3()
    result = medications.dk.stack(
        'id',
        ).convert_dtypes()

    expected = get_df_medications2()

    assert_frame_equal(result, expected)



def test_stack_non_unique():

    medications = get_df_medications3()
    result = medications.dk.stack(
        'id',
        col_pattern = r'(?P<col>.+)_(?P<subid>.+)',
        uid_template = '{uid}',
        cols_keep = None,
        dropna = True,
        sort = True,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications1()
    expected['id'] = expected['id'].astype('string')

    assert_frame_equal(result, expected)
    check_message('WARNING: Result uid col "id" contains non-unique values:')



def test_stack_keep_nas():

    medications = get_df_medications3()
    result = medications.dk.stack(
        'id',
        col_pattern = r'(?P<col>.+)_(?P<subid>.+)',
        uid_template = '{uid}_{subid}',
        cols_keep = None,
        dropna = False,
        sort = True,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications2()
    rows = [
        expected.iloc[[0], :],
        pd.DataFrame([['10002_2', pd.NA, pd.NA, pd.NA]], columns=expected.columns),
        pd.DataFrame([['10002_3', pd.NA, pd.NA, pd.NA]], columns=expected.columns),
        expected.iloc[[1], :],
        expected.iloc[[2], :],
        pd.DataFrame([['20001_3', pd.NA, pd.NA, pd.NA]], columns=expected.columns),
        expected.iloc[[3], :],
        expected.iloc[[4], :],
        expected.iloc[[5], :],
        ]
    expected = pd.concat(rows, axis='index', ignore_index=True).convert_dtypes()

    assert_frame_equal(result, expected)



def test_stack_template():

    medications = get_df_medications3()
    result = medications.dk.stack(
        'id',
        col_pattern = r'(?P<col>.+)_(?P<subid>.+)',
        uid_template = '{uid} #{subid}',
        cols_keep = None,
        dropna = True,
        sort = True,
        verbosity = 3
        ).convert_dtypes()

    expected = get_df_medications2()
    mainid = expected['id'].str.split('_').str[0]
    subid = expected['id'].str.split('_').str[1]
    expected['id'] = mainid + ' #' + subid
    expected = expected.convert_dtypes()

    assert_frame_equal(result, expected)
