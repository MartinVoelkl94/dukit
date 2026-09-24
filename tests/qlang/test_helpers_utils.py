
import pytest
import pandas as pd

from dukit.qlang import symbols
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



@pytest.mark.parametrize('category', [
    'all',
    'syntax',
    'scope',
    'scopes',
    'operator',
    'operators',
    'generic',
    'generics',
    'getter',
    'getters',
    'setter',
    'setters',
    'styler',
    'stylers',
    'viewer',
    'viewers',
    'flag',
    'flags',
    ])
def test_as_df_helpers(category):

    result = symbols.as_df(category)
    styled = symbols.as_df_styled(category)
    cols = [
        'name',
        'lexeme',
        'description',
        'example',
        'category',
        'flags',
        'flags_allowed',
        'scopes_allowed',
        'connectors_allowed',
        ]

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert list(result.columns) == cols

    assert isinstance(styled, pd.io.formats.style.Styler)
    assert not styled.data.empty  #type: ignore
    assert list(styled.data.columns) == cols  #type: ignore



def test_as_df_invalid_category():
    with pytest.raises(ValueError):
        symbols.as_df('does-not-exist')


def test_docstring_helpers():
    doc = 'summary line\n\nExamples\n--------\n>>> alpha\n>>> beta'
    assert symbols._get_description(doc) == 'summary line'
    assert symbols._get_example(doc) == 'alpha\nbeta'
    assert symbols._get_example('summary only') == ''


def test_lexeme_helpers():
    assert symbols._get_lexemes(symbols.GetContains()) == '?'
    assert symbols._get_lexemes(symbols.SetToStr()) == '.tostring\n.tostr'


def test_print_or_display_print(monkeypatch, capsys):
    df_x = pd.DataFrame({'x': [1]})
    monkeypatch.setattr(symbols, 'get_ipython', lambda: object())

    symbols._print_or_display('plain text', df_x)

    out = capsys.readouterr().out
    assert 'plain text' in out
    assert 'x' in out



def test_print_or_display_display(monkeypatch, capsys):
    df_x = pd.DataFrame({'x': [1]})
    displayed = []
    monkeypatch.setattr(
        symbols,
        'get_ipython',
        lambda: ZMQInteractiveShell(),
        )
    monkeypatch.setattr(
        symbols,
        'display',
        displayed.append,
        )

    class ZMQInteractiveShell:
        pass

    symbols._print_or_display('styled text', df_x)
    out = capsys.readouterr().out
    assert 'styled text' in out
    assert len(displayed) == 1

    symbols._print_or_display('ignored', df_x.iloc[0:0])
    out = capsys.readouterr().out
    assert out == ''
