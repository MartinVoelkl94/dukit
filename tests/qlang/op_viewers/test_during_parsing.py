
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

    ('..help', 'scopes:'),
    ('..help', 'flags:'),
    ('..help', 'generic Operators (ops):'),
    ('..help', 'get/select/filter cols/rows/vals:'),
    ('..help', 'set/change/modify cols/rows/vals:'),
    ('..help', 'change style of cols/rows/vals:'),
    ('..help', 'view debug information:'),

    ('.align ..help', 'Operator "StyleAlignement" requires at least 1 args.'),
    ('.align ..help', 'allowed args:'),
    ('.align ..help', 'left'),
    ('.align ..help', 'right'),
    ('.align ..help', 'center'),
    ('.align ..help', 'start'),
    ('.align ..help', 'end'),
    ('.align ..help', 'justify'),

    ('== ..help', 'Operator "GetEquals" requires at least 1 args.'),
    ('== ..help', 'allowed flags:'),
    ('== ..help', 'negate'),
    ('== ..help', 'regex'),
    ('== ..help', 'colref'),
    ('== ..help', 'index'),
    ('== ..help', 'any'),
    ('== ..help', 'all'),
    ('== ..help', 'allcols'),
    ('== ..help', 'strict'),
    ('== ..help', 'str'),
    ('== ..help', 'int'),
    ('== ..help', 'float'),
    ('== ..help', 'num'),
    ('== ..help', 'bool'),
    ('== ..help', 'date'),
    ('== ..help', 'datetime'),

    ])
def test_help(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('% == (name, +strict) ..op', "----Operation 0----\n"),
    ('% == (name, +strict) ..op', "str_matched: '% == (name, +strict) '\n"),
    ('% == (name, +strict) ..op', "connector: 'new'\n"),
    ('% == (name, +strict) ..op', "scope: 'cols'\n"),
    ('% == (name, +strict) ..op', "operator: 'GetEquals'\n"),
    ('% == (name, +strict) ..op', "flags:"),
    ('% == (name, +strict) ..op', "args:"),

    ])
def test_op_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('% == (name, +strict) ..op', "--------Operation 0--------\n"),
    ('% == (name, +strict) ..op', "str_matched: '% == (name, +strict) '\n"),
    ('% == (name, +strict) ..op', "connector: 'new'\n"),
    ('% == (name, +strict) ..op', "scope: 'cols'\n"),
    ('% == (name, +strict) ..op', "operator: 'GetEquals'\n"),
    ('% == (name, +strict) ..op', "flags:"),
    ('% == (name, +strict) ..op', "args:"),

    ('% == (name, +strict) ..op', "connectors_allowed:"),
    ('% == (name, +strict) ..op', "scopes_allowed:"),
    ('% == (name, +strict) ..op', "flags_allowed:"),
    ('% == (name, +strict) ..op', "args_allowed:"),
    ('% == (name, +strict) ..op', "args_min:"),
    ('% == (name, +strict) ..op', "args_max:"),

    ])
def test_op_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('% == (name, +strict) ?j ..ops', "----Operation 0----\n"),
    ('% == (name, +strict) ?j ..ops', "str_matched: '% == (name, +strict) '\n"),
    ('% == (name, +strict) ?j ..ops', "connector: 'new'\n"),
    ('% == (name, +strict) ?j ..ops', "scope: 'cols'\n"),
    ('% == (name, +strict) ?j ..ops', "operator: 'GetEquals'\n"),
    ('% == (name, +strict) ?j ..ops', "flags:"),
    ('% == (name, +strict) ?j ..ops', "args:"),

    ])
def test_ops_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('% == (name, +strict) ?j ..ops', "--------Operation 0--------\n"),
    ('% == (name, +strict) ?j ..ops', "str_matched: '% == (name, +strict) '\n"),
    ('% == (name, +strict) ?j ..ops', "connector: 'new'\n"),
    ('% == (name, +strict) ?j ..ops', "scope: 'cols'\n"),
    ('% == (name, +strict) ?j ..ops', "operator: 'GetEquals'\n"),
    ('% == (name, +strict) ?j ..ops', "flags:"),
    ('% == (name, +strict) ?j ..ops', "args:"),

    ('% == (name, +strict) ?j ..ops', "connectors_allowed:"),
    ('% == (name, +strict) ?j ..ops', "scopes_allowed:"),
    ('% == (name, +strict) ?j ..ops', "flags_allowed:"),
    ('% == (name, +strict) ?j ..ops', "args_allowed:"),
    ('% == (name, +strict) ?j ..ops', "args_min:"),
    ('% == (name, +strict) ?j ..ops', "args_max:"),

    ])
def test_ops_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('..query', '--------Query object [q]--------\n'),
    ('..query', '>>> q.code'),
    ('..query', '>>> q.tokens'),
    ('..query', '>>> q.ops'),
    ('..query', '>>> q.df'),
    ('..query', '>>> q.scan()  #scan code into tokens\n'),
    ('..query', '>>> q.parse()  #parse tokens into ops\n'),
    ('..query', '>>> q.run()  #run ops on the df\n'),
    ('..query', '>>> q.result'),
    ('..query', '>>> q.styled'),
    ('..query', '--------Query object end--------'),


    ])
def test_query_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

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

    ])
def test_query_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('%..token', "<'ScopeColsNew' '%'>"),
    ('%name..token', "<'Literal' 'name'>"),

    ])
def test_token_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('%..token', "----Token 1----\n"),
    ('%..token', "name: 'ScopeColsNew'\n"),
    ('%..token', "category: 'scope'\n"),
    ('%..token', "regex: ('%',)\n"),
    ('%..token', "linenum: 1\n"),
    ('%..token', "str_matched: '%'\n"),
    ('%..token', "literal: ''\n"),


    ('%name..token', "----Token 2----\n"),
    ('%name..token', "name: 'Literal'\n"),
    ('%name..token', "category: 'syntax'\n"),
    ('%name..token', "regex:"),
    ('%name..token', "linenum: 1\n"),
    ('%name..token', "str_matched: 'name'\n"),
    ('%name..token', "literal: 'name'\n"),

    ])
def test_token_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('%name..tokens', "<'ScopeColsNew' '%'>"),
    ('%name..tokens', "<'Literal' 'name'>"),

    ])
def test_tokens_repr(capsys, code, txt):
    df.dk.qs(code, 3)
    out = capsys.readouterr().out
    assert txt in out



@pytest.mark.parametrize('code, txt', [

    ('%name..tokens', "----Token 1----\n"),
    ('%name..tokens', "name: 'ScopeColsNew'\n"),
    ('%name..tokens', "category: 'scope'\n"),
    ('%name..tokens', "regex: ('%',)\n"),
    ('%name..tokens', "linenum: 1\n"),
    ('%name..tokens', "str_matched: '%'\n"),
    ('%name..tokens', "literal: ''\n"),
    ('%name..tokens', "----Token 2----\n"),
    ('%name..tokens', "name: 'Literal'\n"),
    ('%name..tokens', "category: 'syntax'\n"),
    ('%name..tokens', "regex:"),
    ('%name..tokens', "linenum: 1\n"),
    ('%name..tokens', "str_matched: 'name'\n"),
    ('%name..tokens', "literal: 'name'\n"),

    ])
def test_tokens_str(capsys, code, txt):
    df.dk.qs(code, 4)
    out = capsys.readouterr().out
    assert txt in out
