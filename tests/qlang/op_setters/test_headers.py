
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




def test_cols1():
    code = r'name  %=full_name  %'
    result = df.dk.qr(code).result
    expected = get_df().rename(columns={'name': 'full_name'})
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_cols2():
    code = r'name  /age  %=renamed  %'
    result = df.dk.qr(code).result
    mapping = {
        'name': 'renamed',
        'age': 'renamed',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_cols3():
    code = r"""
    name %=full_name
    'date of birth' %=dob
    %
    """
    result = df.dk.qr(code).result
    mapping = {
        'name': 'full_name',
        'date of birth': 'dob',
        }
    expected = get_df().rename(columns=mapping)
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)
