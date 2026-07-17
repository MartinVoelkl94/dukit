
import pytest

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




params = [
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
]
@pytest.mark.parametrize('code, txt', params)
def test_viewers_during_execution(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out




params = [
    ('..help', 'available scopes:'),
    ('..help', 'generic Operators (ops):'),
    ('..help', 'get/select/filter cols/rows/vals:'),
    ('..help', 'set/change/modify cols/rows/vals:'),
    ('..help', 'change style of cols/rows/vals:'),
    ('..help', 'view debug information:'),

    ('..query', '----------Query object [q]----------'),
    ('..query', '>>> q.code'),
    ('..query', '>>> q.tokens'),
    ('..query', '>>> q.ops'),
    ('..query', '>>> q.op'),
    ('..query', '>>> q.df'),
    ('..query', '>>> q.mask_cols'),
    ('..query', '>>> q.mask_rows'),
    ('..query', '>>> q.mask_vals'),
    ('..query', '>>> q.masks_saved'),
    ('..query', '>>> q.style_cols'),
    ('..query', '>>> q.style_rows'),
    ('..query', '>>> q.style_vals'),
    ('..query', '----------Query object end----------'),

    ('..ops', ''),
    ('..op', ''),

    ('..tokens', ''),
    ('..token', ''),
]
@pytest.mark.parametrize('code, txt', params)
def test_viewers_during_parsing(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out
