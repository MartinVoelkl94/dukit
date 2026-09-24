
import os
import pytest
import pandas as pd
import dukit as dk



def test_cd(tmp_path):
    src = tmp_path / 'src'
    target = tmp_path / 'target'
    src.mkdir()
    target.mkdir()
    os.chdir(src)

    dk.os.cd(str(target), verbosity=0)
    assert os.getcwd() == str(target)

    dk.os.cd(str(src), verbosity=0)
    assert os.getcwd() == str(src)


@pytest.mark.parametrize('path', [None, '', '.', '..'])
def test_cd_special_paths(path, tmp_path):
    os.chdir(tmp_path)
    original = os.getcwd()

    dk.os.cd(path, verbosity=0)
    if path == '..':
        expected = os.path.dirname(original)
    else:
        expected = original
    assert os.getcwd() == expected



def test_cp(tmp_path):
    src = tmp_path / 'src.txt'
    dest = tmp_path / 'dest.txt'
    copied = tmp_path / 'copied'
    src.write_text('src')
    copied.mkdir()

    dk.os.cp(src, dest, verbosity=0)
    assert dest.read_text() == 'src'

    src.write_text('updated')
    dk.os.cp(src, dest, verbosity=0)
    assert dest.read_text() == 'updated'

    dk.os.cp(src, copied, verbosity=0)
    assert (copied / src.name).read_text() == 'updated'



def test_cp_dir(tmp_path):
    dir = tmp_path / 'dir'
    file_nested = dir / 'nested.txt'
    dir_copied = tmp_path / 'copied_dir'

    dir.mkdir()
    file_nested.write_text('nested')

    dk.os.cp(dir, dir_copied, verbosity=0)
    assert (dir_copied / 'nested.txt').read_text() == 'nested'


def test_fetch(tmp_path):
    direct = tmp_path / 'direct.txt'
    direct.write_text('direct')
    result = dk.os.fetch(direct, verbosity=0)
    assert result == direct



def test_fetch_before(tmp_path):
    first = tmp_path / 'report2020-01-01.csv'
    latest = tmp_path / 'report2020-01-03.csv'
    ignored1 = tmp_path / 'report-not-a-date.csv'
    ignored2 = tmp_path / 'report2020bad.csv'

    first.write_text('first')
    latest.write_text('latest')
    ignored1.write_text('ignored')
    ignored2.write_text('ignored')

    result = dk.os.fetch(
        tmp_path / 'report',
        before='2020-01-03',
        verbosity=0,
        )
    assert result == str(first)



@pytest.mark.parametrize(
    'before',
    ['today', 'this day', 'this week', 'this month', 'this year'],
    )
def test_fetch_cutoff_options(before, tmp_path):
    with pytest.raises(FileNotFoundError, match='no timestamped files'):
        dk.os.fetch(tmp_path / 'missing', before=before, verbosity=0)


def test_fetch_latest(tmp_path):
    first = tmp_path / 'report2020-01-01.csv'
    latest = tmp_path / 'report2020-01-03.csv'
    ignored1 = tmp_path / 'report-not-a-date.csv'
    ignored2 = tmp_path / 'report2020bad.csv'

    first.write_text('first')
    latest.write_text('latest')
    ignored1.write_text('ignored')
    ignored2.write_text('ignored')

    result = dk.os.fetch(tmp_path / 'report', verbosity=0)
    assert result == str(latest)


def test_fetch_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match='no timestamped files'):
        dk.os.fetch(tmp_path / 'missing', verbosity=0)


def test_isdir(tmp_path):
    file = tmp_path / 'file.txt'
    file.write_text('text')
    assert dk.os.isdir(tmp_path)
    assert not dk.os.isdir(file)


def test_isfile(tmp_path):
    file = tmp_path / 'file.txt'
    file.write_text('text')
    assert not dk.os.isfile(tmp_path)
    assert dk.os.isfile(file)


def test_ispath(tmp_path):
    file = tmp_path / 'file.txt'
    path_fake = tmp_path / 'missing'
    file.write_text('text')

    assert dk.os.ispath(tmp_path)
    assert dk.os.ispath(file)
    assert not dk.os.ispath(path_fake)



def test_ls_lsr(tmp_path):
    dir_nested = tmp_path / 'nested'
    file_root = tmp_path / 'root.txt'
    file_nested = dir_nested / 'nested.txt'

    dir_nested.mkdir()
    file_root.write_text('root')
    file_nested.write_text('nested')

    result = dk.os.ls(str(tmp_path))
    assert isinstance(result, pd.DataFrame)
    assert set(result['name']) == {'nested', 'root.txt'}
    assert result.loc[result['name'] == 'nested', 'type'].iloc[0] == 'dir'
    assert result.loc[result['name'] == 'root.txt', 'type'].iloc[0] == '.txt'
    assert result.loc[result['name'] == 'root.txt', 'size'].iloc[0] == 4
    assert (
        result.loc[result['name'] == 'root.txt', 'permissions']
        .notna()
        .all()
        )

    recursive = dk.os.lsr(str(tmp_path))
    assert set(recursive['name']) == {'root.txt', 'nested.txt'}
    assert dk.os.ls(str(tmp_path), recursive=True).equals(recursive)



def test_ls_default_path(tmp_path):
    os.chdir(tmp_path)
    file = tmp_path / 'file.txt'
    file.write_text('text')
    result = dk.os.ls()
    assert result['name'].to_list() == [file.name]



def test_mv(tmp_path):
    src = tmp_path / 'src.txt'
    src.write_text('src')
    dest = tmp_path / 'dest.txt'

    dk.os.mv(src, dest, verbosity=0)
    assert dest.read_text() == 'src'
    assert not src.exists()


def test_mv_dir(tmp_path):
    dir = tmp_path / 'dir'
    file_nested = dir / 'nested.txt'
    dir_moved = tmp_path / 'moved_dir'

    dir.mkdir()
    file_nested.write_text('nested')

    dk.os.mv(dir, dir_moved, verbosity=0)
    assert (dir_moved / 'nested.txt').read_text() == 'nested'
    assert not dir.exists()


def test_mkdir(tmp_path):
    dir_new = tmp_path / 'new'

    dk.os.mkdir(dir_new, verbosity=0)
    assert dir_new.is_dir()

    dk.os.mkdir(dir_new, verbosity=0)
    assert dir_new.is_dir()


def test_pwd(tmp_path):
    os.chdir(tmp_path)
    assert dk.os.pwd() == str(tmp_path)
