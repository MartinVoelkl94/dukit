
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




def test_copy1():
    code = 'name   .copy  %'
    result = qr(df, code).result
    expected = get_df()
    expected['name1'] = expected['name']
    assert_frame_equal(result, expected)




def test_copy2():
    code = 'name   .copy  .copy  %'
    result = qr(df, code).result
    expected = get_df()
    expected['name1'] = expected['name']
    expected['name11'] = expected['name1']
    assert_frame_equal(result, expected)




def test_copy3():
    code = 'name   .copy new  %'
    result = qr(df, code).result
    expected = get_df()
    expected['new'] = expected['name']
    assert_frame_equal(result, expected)
