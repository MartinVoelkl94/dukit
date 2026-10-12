
import pandas as pd

from dukit import deduplicate



def test_list():
    obj = [1]
    expected = ['1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list1():
    obj = [1, 1]
    expected = ['1', '1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list2():
    obj = [1, 2, 2,]
    expected = ['1', '2', '2_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list3():
    obj = [1, 2, 2, 3, 3, 3]
    expected = ['1', '2', '2_1', '3', '3_1', '3_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list4():
    obj = [3, 1, 3, 2, 3, 2]
    expected = ['3', '1', '3_1', '2', '3_2', '2_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list5():
    obj = [1, 1, '1_1']
    expected = ['1', '1_1', '1_1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_list6():
    obj = ['1_1', 1, '1_1_1', 1, '1_1']
    expected = ['1_1', '1', '1_1_1', '1_1_1_1', '1_1_1_1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore




def test_series():
    obj = pd.Series([1])
    expected = pd.Series(['1'])
    result = deduplicate(
        obj,
        name='test_series',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series1():
    obj = pd.Series([1, 1])
    expected = pd.Series(['1', '1_1'])
    result = deduplicate(
        obj,
        name='test_series1',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series2():
    obj = pd.Series([1, 2, 2])
    expected = pd.Series(['1', '2', '2_1'])
    result = deduplicate(
        obj,
        name='test_series2',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series3():
    obj = pd.Series([1, 2, 2, 3, 3, 3])
    expected = pd.Series(['1', '2', '2_1', '3', '3_1', '3_2'])
    result = deduplicate(
        obj,
        name='test_series3',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series4():
    obj = pd.Series([3, 1, 3, 2, 3, 2])
    expected = pd.Series(['3', '1', '3_1', '2', '3_2', '2_1'])
    result = deduplicate(
        obj,
        name='test_series4',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series5():
    obj = pd.Series([1, 1, '1_1'])
    expected = pd.Series(['1', '1_1', '1_1_1'])
    result = deduplicate(
        obj,
        name='test_series5',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series6():
    obj = pd.Series(['1_1', 1, '1_1_1', 1, '1_1'])
    expected = pd.Series(['1_1', '1', '1_1_1', '1_1_1_1', '1_1_1_1_1'])
    result = deduplicate(
        obj,
        name='test_series6',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series_index():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'c'])
    expected = pd.Series(['1', '1_1', '1_1_1'], index=['a', 'b', 'c'])
    result = deduplicate(
        obj,
        name='test_series_index',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_series_index1():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'b'])
    expected = pd.Series(['1', '1_1', '1_1_1'], index=['a', 'b', 'b_1'])
    result = deduplicate(
        obj,
        name='test_series_index1',
        rename_all=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'



def test_rename_all_list():
    obj = [1]
    expected = ['1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list1():
    obj = [1, 1]
    expected = ['1_1', '1_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list2():
    obj = [1, 2, 2,]
    expected = ['1_1', '2_1', '2_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list3():
    obj = [1, 2, 2, 3, 3, 3]
    expected = ['1_1', '2_1', '2_2', '3_1', '3_2', '3_3']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list4():
    obj = [3, 1, 3, 2, 3, 2]
    expected = ['3_1', '1_1', '3_2', '2_1', '3_3', '2_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list5():
    obj = [1, 1, '1_1']
    expected = ['1_1', '1_2', '1_1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_rename_all_list6():
    obj = ['1_1', 1, '1_1_1', 1, '1_1']
    expected = ['1_1_1', '1_1', '1_1_1_1', '1_2', '1_1_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore




def test_rename_all_series():
    obj = pd.Series([1])
    expected = pd.Series(['1_1'])
    result = deduplicate(
        obj,
        name='test_series',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series1():
    obj = pd.Series([1, 1])
    expected = pd.Series(['1_1', '1_2'])
    result = deduplicate(
        obj,
        name='test_series1',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series2():
    obj = pd.Series([1, 2, 2])
    expected = pd.Series(['1_1', '2_1', '2_2'])
    result = deduplicate(
        obj,
        name='test_series2',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series3():
    obj = pd.Series([1, 2, 2, 3, 3, 3])
    expected = pd.Series(['1_1', '2_1', '2_2', '3_1', '3_2', '3_3'])
    result = deduplicate(
        obj,
        name='test_series3',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series4():
    obj = pd.Series([3, 1, 3, 2, 3, 2])
    expected = pd.Series(['3_1', '1_1', '3_2', '2_1', '3_3', '2_2'])
    result = deduplicate(
        obj,
        name='test_series4',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series5():
    obj = pd.Series([1, 1, '1_1'])
    expected = pd.Series(['1_1', '1_2', '1_1_1'])
    result = deduplicate(
        obj,
        name='test_series5',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series6():
    obj = pd.Series(['1_1', 1, '1_1_1', 1, '1_1'])
    expected = pd.Series(['1_1_1', '1_1', '1_1_1_1', '1_2', '1_1_2'])
    result = deduplicate(
        obj,
        name='test_series6',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series_index():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'c'])
    expected = pd.Series(['1_1', '1_2', '1_1_1'], index=['a', 'b', 'c'])
    result = deduplicate(
        obj,
        name='test_series_index',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_rename_all_series_index1():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'b'])
    expected = pd.Series(['1_1', '1_2', '1_1_1'], index=['a_1', 'b_1', 'b_2'])
    result = deduplicate(
        obj,
        name='test_series_index1',
        rename_all=True,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'



def test_start_at_0_list():
    obj = [1]
    expected = ['1_0']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list1():
    obj = [1, 1]
    expected = ['1_0', '1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list2():
    obj = [1, 2, 2,]
    expected = ['1_0', '2_0', '2_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list3():
    obj = [1, 2, 2, 3, 3, 3]
    expected = ['1_0', '2_0', '2_1', '3_0', '3_1', '3_2']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list4():
    obj = [3, 1, 3, 2, 3, 2]
    expected = ['3_0', '1_0', '3_1', '2_0', '3_2', '2_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list5():
    obj = [1, 1, '1_1']
    expected = ['1_0', '1_1', '1_1_0']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore


def test_start_at_0_list6():
    obj = ['1_1', 1, '1_1_1', 1, '1_1']
    expected = ['1_1_0', '1_0', '1_1_1_0', '1_1', '1_1_1']
    result = deduplicate(
        obj,
        name='test_list',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result == expected, f'EXPECTED: {expected}\nRESULT: {result}'  #type: ignore




def test_start_at_0_series():
    obj = pd.Series([1])
    expected = pd.Series(['1_0'])
    result = deduplicate(
        obj,
        name='test_series',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series1():
    obj = pd.Series([1, 1])
    expected = pd.Series(['1_0', '1_1'])
    result = deduplicate(
        obj,
        name='test_series1',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series2():
    obj = pd.Series([1, 2, 2])
    expected = pd.Series(['1_0', '2_0', '2_1'])
    result = deduplicate(
        obj,
        name='test_series2',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series3():
    obj = pd.Series([1, 2, 2, 3, 3, 3])
    expected = pd.Series(['1_0', '2_0', '2_1', '3_0', '3_1', '3_2'])
    result = deduplicate(
        obj,
        name='test_series3',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series4():
    obj = pd.Series([3, 1, 3, 2, 3, 2])
    expected = pd.Series(['3_0', '1_0', '3_1', '2_0', '3_2', '2_1'])
    result = deduplicate(
        obj,
        name='test_series4',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series5():
    obj = pd.Series([1, 1, '1_1'])
    expected = pd.Series(['1_0', '1_1', '1_1_0'])
    result = deduplicate(
        obj,
        name='test_series5',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series6():
    obj = pd.Series(['1_1', 1, '1_1_1', 1, '1_1'])
    expected = pd.Series(['1_1_0', '1_0', '1_1_1_0', '1_1', '1_1_1'])
    result = deduplicate(
        obj,
        name='test_series6',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series_index():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'c'])
    expected = pd.Series(['1_0', '1_1', '1_1_0'], index=['a', 'b', 'c'])
    result = deduplicate(
        obj,
        name='test_series_index',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'


def test_start_at_0_series_index1():
    obj = pd.Series([1, 1, '1_1'], index=['a', 'b', 'b'])
    expected = pd.Series(['1_0', '1_1', '1_1_0'], index=['a_0', 'b_0', 'b_1'])
    result = deduplicate(
        obj,
        name='test_series_index1',
        rename_all=True,
        start_at_1=False,
        verbosity=3,
        )
    assert result.equals(expected), f'EXPECTED: {expected}\nRESULT: {result}'
