
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




def test_cols1():
    code = '%.sort'
    result = df.dk.qr(code).result
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
    result = df.dk.qr(code).result
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
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_rows2():
    code = r'%%!.sort'
    result = df.dk.qr(code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_vals1():
    code = r'ID  .sort  %'
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_vals2():
    code = r'ID  !.sort  %'
    result = df.dk.qr(code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)




def test_update_masks_cols1():
    code = r"""
    .save(1)
    %.sort
    %:load(1)
    """
    result = df.dk.qr(code).result
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



def test_update_masks_cols2():
    code = r"""
    .save(1)
    %!.sort
    %:load(1)
    """
    result = df.dk.qr(code).result
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



def test_update_masks_rows1():
    code = r'%%.sort'
    code = r"""
    .save(1)
    %%.sort
    %%:load(1)
    """
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_update_masks_rows2():
    code = r"""
    .save(1)
    %%!.sort
    %%:load(1)
    """
    result = df.dk.qr(code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_update_masks_vals1():
    code = r"""
    .save(1)
    ID  .sort  %
    %%:load(1)
    """
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)



def test_update_masks_vals2():
    code = r"""
    .save(1)
    ID  !.sort  %
    %%:load(1)
    """
    result = df.dk.qr(code).result
    rows = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    expected = get_df()
    expected = expected.loc[rows, :]
    assert_frame_equal(result, expected)




def test_update_styles_cols1():
    code = r"""
    age  %.color(orange)
    %
    %.sort
    """
    result = df.dk.qr(code).style_cols.to_list()
    expected = [
        '',
        'color: orange;',
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
        ]
    assert result == expected



def test_update_styles_cols2():
    code = r"""
    age  %.color(orange)
    %
    %!.sort
    """
    result = df.dk.qr(code).style_cols.to_list()
    expected = [
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
        'color: orange;',
        '',
        ]
    assert result == expected



def test_update_styles_rows1():
    code = r"""
    %%§1  %%.color(orange)
    %%
    %%.sort
    """
    result = df.dk.qr(code).style_rows.to_list()
    expected = [
        '',
        'color: orange;',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    assert result == expected



def test_update_styles_rows2():
    code = r"""
    %%§1  %%.color(orange)
    %%
    %%!.sort
    """
    result = df.dk.qr(code).style_rows.to_list()
    expected = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        'color: orange;',
        '',
        ]
    assert result == expected



def test_update_styles_vals1():
    code = r"""
    name  =='Bob Brown' .color(orange)
    %%
    .sort
    """
    result = df.dk.qr(code).style_vals['name'].to_list()
    expected = [
        '',
        'color: orange;',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    assert result == expected



def test_update_styles_vals2():
    code = r"""
    name  =='Bob Brown' .color(orange)
    %%
    !.sort
    """
    result = df.dk.qr(code).style_vals['name'].to_list()
    expected = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        'color: orange;',
        '',
        ]
    assert result == expected
