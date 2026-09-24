
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





def test_rows1():
    code = r"""
    name
        %%=="john doe"
            =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 10], 'name'] = 'deleted'
    assert_frame_equal(result, expected)



def test_rows2():
    code = r"""
    name
        %%=="john doe"
    /age
        %%%=deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 10], ['name', 'age']] = 'deleted'
    assert_frame_equal(result, expected)



def test_rows3():
    code = r"""
    name
        %%=="john doe"
        %
        =deleted
    /age
        //30
        %
        =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['ID'] = expected['ID'].astype('object')
    expected.loc[[0, 1, 10], :] = 'deleted'
    assert_frame_equal(result, expected)



def test_rows4():
    code = r"""
    name
        %%=="john doe"
    /age
        //30
        %%%:all
        =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 1, 10], ['name', 'age']] = 'deleted'
    assert_frame_equal(result, expected)



def test_rows5():
    code = r"""
    name  = age +colref
    %
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['name'] = expected['age']
    assert_frame_equal(result, expected)



def test_rows6():
    code = r"""
    name  = @age
    %
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['name'] = expected['age']
    assert_frame_equal(result, expected)
