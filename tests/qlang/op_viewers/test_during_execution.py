
import pytest

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



@pytest.mark.parametrize('code, txt', [

    ('.masks', 'mask_cols:'),
    ('.masks', 'mask_rows:'),
    ('.masks', 'mask_vals:'),
    ('.masks(arg)', 'arg'),

    ('.cols', 'mask_cols:'),
    ('.rows', 'mask_rows:'),
    ('.vals', 'mask_vals:'),
    ('.cols(arg)', 'arg'),
    ('.rows(arg)', 'arg'),
    ('.vals(arg)', 'arg'),

    ])
def test_masks(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('name  .print()', 'name'),
    ('name  .print()', 'John Doe'),
    ('name  .print()', 'Jane Smith'),
    ('name  .print()', 'Alice Johnson'),
    ('name  .print()', 'Bob Brown'),
    ('name  .print()', 'eva white'),
    ('name  .print()', 'Frank miller'),
    ('name  .print()', 'Grace TAYLOR'),
    ('name  .print()', 'Harry Clark'),
    ('name  .print()', 'IVY GREEN'),
    ('name  .print()', 'JAck Williams'),
    ('name  .print()', 'john Doe'),

    ('name  .print(marker)', 'marker'),
    ('name  .print(marker)', 'name'),
    ('name  .print(marker)', 'John Doe'),
    ('name  .print(marker)', 'Jane Smith'),
    ('name  .print(marker)', 'Alice Johnson'),
    ('name  .print(marker)', 'Bob Brown'),
    ('name  .print(marker)', 'eva white'),
    ('name  .print(marker)', 'Frank miller'),
    ('name  .print(marker)', 'Grace TAYLOR'),
    ('name  .print(marker)', 'Harry Clark'),
    ('name  .print(marker)', 'IVY GREEN'),
    ('name  .print(marker)', 'JAck Williams'),
    ('name  .print(marker)', 'john Doe'),

    ])
def test_print(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('.query', '--------Query object [q]--------\n'),
    ('.query', '>>> q.code'),
    ('.query', '>>> q.tokens'),
    ('.query', '>>> q.ops'),
    ('.query', '>>> q.df'),
    ('.query', '>>> q.scan()  #scan code into tokens\n'),
    ('.query', '>>> q.parse()  #parse tokens into ops\n'),
    ('.query', '>>> q.run()  #run ops on the df\n'),
    ('.query', '>>> q.result'),
    ('.query', '>>> q.styled'),
    ('.query', '--------Query object end--------'),

    ])
def test_query_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('.query', '----------Query object [q]----------'),
    ('.query', '>>> q.code'),
    ('.query', '>>> q.tokens'),
    ('.query', '>>> q.ops'),
    ('.query', '>>> q.op'),
    ('.query', '>>> q.df'),
    ('.query', '>>> q.mask_cols'),
    ('.query', '>>> q.mask_rows'),
    ('.query', '>>> q.mask_vals'),
    ('.query', '>>> q.masks_saved'),
    ('.query', '>>> q.style_cols'),
    ('.query', '>>> q.style_rows'),
    ('.query', '>>> q.style_vals'),
    ('.query(arg)', 'arg'),
    ('.query', '----------Query object end----------'),

    ])
def test_query_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out
