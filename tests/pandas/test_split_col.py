
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import get_df, log


def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



def test_basic():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1=None,
        new2='last name',
        )

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected.drop(columns=['name'], inplace=True)
    expected.insert(loc=1, column='name', value=col_new1)
    expected.insert(loc=2, column='last name', value=col_new2)

    assert_frame_equal(result, expected)



def test_rename():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1='first name',
        new2='last name',
        )

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected.drop(columns=['name'], inplace=True)
    expected.insert(loc=1, column='first name', value=col_new1)
    expected.insert(loc=2, column='last name', value=col_new2)

    assert_frame_equal(result, expected)



def test_wrong_sep():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=';',
        new1=None,
        new2='last name',
        )

    expected = get_df()
    col_new1 = pd.Series([
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
        'john Doe',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ],
        dtype='string',
        )
    expected['name'] = col_new1
    expected.insert(loc=2, column='last name', value=col_new2)

    assert_frame_equal(result, expected)



def test_non_existent_col():

    df = get_df()
    result = df.dk.split_col(
        col='non_existent_col',
        sep=' ',
        new1=None,
        new2='last name',
        )

    expected = get_df()

    assert_frame_equal(result, expected)
    check_message('ERROR: no col named "non_existent_col" found')



def test_non_unique_col():

    df = get_df()
    df.rename(columns={'ID': 'name'}, inplace=True)
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1=None,
        new2='last name',
        )

    expected = get_df()
    expected.rename(columns={'ID': 'name'}, inplace=True)

    assert_frame_equal(result, expected)
    check_message('ERROR: multiple cols named "name" found')



def test_new1_already_exists():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1='ID',
        new2='last name',
        )

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected.drop(columns=['name'], inplace=True)
    expected.insert(loc=1, column='ID1', value=col_new1)
    expected.insert(loc=2, column='last name', value=col_new2)

    assert_frame_equal(result, expected)



def test_new2_already_exists():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1=None,
        new2='ID',
        )

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected.drop(columns=['name'], inplace=True)
    expected.insert(loc=1, column='name', value=col_new1)
    expected.insert(loc=2, column='ID1', value=col_new2)

    assert_frame_equal(result, expected)



def test_both_already_exist():

    df = get_df()
    result = df.dk.split_col(
        col='name',
        sep=' ',
        new1='ID',
        new2='ID',
        )

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected.drop(columns=['name'], inplace=True)
    expected.insert(loc=1, column='ID1', value=col_new1)
    expected.insert(loc=2, column='ID2', value=col_new2)

    assert_frame_equal(result, expected)
