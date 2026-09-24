
import re
import pytest
import pandas as pd
import dukit as dk



def test_build_log_context():
    df = pd.DataFrame({'value': [1]})
    series = pd.Series([1])

    result = dk.utils._build_log_context(
        'test()',
        verbosity=3,
        df=df,
        series=series,
        values=[1, 'two'],
        mapping={'value': 1},
        text='two',
        )

    assert result.startswith('function: test()\n')
    assert 'df:' in result
    assert 'series:' in result
    assert 'values: [' in result
    assert "'two'" in result
    assert "mapping: {'value': 1}" in result
    assert "text: 'two'" in result

    result = dk.utils._build_log_context(
        'test()',
        verbosity=4,
        text='two',
        )
    assert 'text: two' in result



@pytest.mark.parametrize(
    'strategy, taken, expected',
    [
        ('increment', {'name', 'name1', 'name2'}, 'name3'),
        ('increment', set(), 'name'),
        ('prefix=pre_', {'name', 'pre_name'}, 'pre_pre_name'),
        ('suffix=_copy', {'name', 'name_copy'}, 'name_copy_copy'),
        ('datestamp', set(), None),
    ],
    )
def test_ensure_unique_string(strategy, taken, expected):
    result = dk.utils.ensure_unique_string('name', taken, strategy)

    if expected is None:
        assert re.fullmatch(r'name_\d{4}_\d{2}_\d{2}', result)
    else:
        assert result == expected



def test_ensure_unique_string_random(monkeypatch):
    monkeypatch.setattr(
        dk.utils.random,
        'choices',
        lambda chars, k: list('ABC123'),
        )
    result = dk.utils.ensure_unique_string('name', {'name'}, 'random')
    assert result == 'name_ABC123'


def test_ensure_unique_string_timestamp(monkeypatch):
    result = dk.utils.ensure_unique_string(
        'name',
        {'name', 'name_2020_01_02_03h04m05s'},
        'timestamp',
        )
    assert re.fullmatch(
        r'name_\d{4}_\d{2}_\d{2}_\d{2}h\d{2}m\d{2}s',
        result,
        )


def test_ensure_unique_string_invalid_strategy():
    with pytest.raises(ValueError, match='Unknown strategy'):
        dk.utils.ensure_unique_string('name', set(), 'unknown')


def test_log_empty(capsys):
    dk.utils.log(clear=True, verbosity=1)
    capsys.readouterr()

    result = dk.utils.log()
    assert isinstance(result, pd.io.formats.style.Styler)
    assert result.data.empty  # type: ignore



def test_log_empty_and_clear(capsys):
    dk.utils.log(clear=True, verbosity=1)
    capsys.readouterr()

    dk.utils.log('INFO: message', verbosity=0)
    assert len(dk.utils.log().data) == 0  # type: ignore
    assert capsys.readouterr().out == ''

    dk.utils.log('INFO: message', verbosity=5)
    assert len(dk.utils.log().data) == 1  # type: ignore
    assert 'message' in capsys.readouterr().out

    dk.utils.log(clear=True, verbosity=3)
    assert 'cleared all logs' in capsys.readouterr().out
    assert dk.utils.log().data.empty  # type: ignore



@pytest.mark.parametrize(
    'text, level',
    [
        ('TRACE: trace', 'TRACE'),
        ('DEBUG - debug', 'DEBUG'),
        ('INFO message', 'INFO'),
        ('WARNING: warning', 'WARNING'),
        ('ERROR-error', 'ERROR'),
        ('plain message', 'INFO'),
    ],
    )
def test_log_levels(text, level, capsys):
    dk.utils.log(clear=True, verbosity=1)
    capsys.readouterr()

    dk.utils.log(text, verbosity=5)

    result = dk.utils.log().data  # type: ignore
    assert result.iloc[-1]['level'] == level
    assert capsys.readouterr().out



def test_log_display_branch(monkeypatch):
    displayed = []

    class ZMQInteractiveShell:
        pass

    monkeypatch.setattr(dk.utils, 'get_ipython', lambda: ZMQInteractiveShell())
    monkeypatch.setattr(dk.utils, 'display', displayed.append)

    dk.utils.log(clear=True, verbosity=1)
    dk.utils.log('INFO: <message>', context='line\nnext', verbosity=3)

    assert len(displayed) == 1
    assert len(dk.utils.log().data) == 1  # type: ignore
    assert dk.utils.log().data.iloc[0]['text'] == '&lt;message&gt;'  # type: ignore
    assert dk.utils.log().data.iloc[0]['context'] == 'line<br>next'  # type: ignore


def test_now():
    result = dk.utils.now('%Y-%m-%d')
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', result)
