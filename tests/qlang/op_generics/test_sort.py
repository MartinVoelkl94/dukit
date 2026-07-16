
from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    qr,
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




def test_cols1():
    code = '%.sort'
    result = qr(df, code).result
    cols = [
        'ID',
        'age',
        'bp diastole',
        'bp systole',
        'cholesterol',
        'date of birth',
        'diabetes',
        'dose',
        'gender',
        'height',
        'name',
        'weight',
        ]
    expected = get_df()
    expected = expected.loc[:, cols]
    assert_frame_equal(result, expected)



def test_cols2():
    code = '%!.sort'
    result = qr(df, code).result
    cols = [
        'weight',
        'name',
        'height',
        'gender',
        'dose',
        'diabetes',
        'date of birth',
        'cholesterol',
        'bp systole',
        'bp diastole',
        'age',
        'ID',
        ]
    expected = get_df()
    expected = expected.loc[:, cols]
    assert_frame_equal(result, expected)



def test_rows1():
    code = r'%%.sort'
    result = qr(df, code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_rows2():
    code = r'%%!.sort'
    result = qr(df, code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_vals1():
    code = r'ID  .sort  %'
    result = qr(df, code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_vals2():
    code = r'ID  !.sort  %'
    result = qr(df, code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)
