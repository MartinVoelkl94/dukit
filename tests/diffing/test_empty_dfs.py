
import pandas as pd
import dukit as dk
from pandas.testing import assert_frame_equal


def test_both():

    result = dk.diff(
        pd.DataFrame(),
        pd.DataFrame(),
        verbosity=0,
        ).show().data  #type:ignore

    expected = pd.DataFrame({'diff': ['empty dfs']})

    assert_frame_equal(result, expected)



def test_added():

    new = pd.DataFrame({'uid': ['x'], 'value': [1]})

    result = dk.diff(
        pd.DataFrame(),
        new,
        verbosity=0,
        ).show().data  #type:ignore

    expected = pd.DataFrame({
        'diff': ['df added'],
        'uid': ['x'],
        'value': [1],
        })

    assert_frame_equal(result, expected)



def test_removed():

    old = pd.DataFrame({'uid': ['x'], 'value': [1]})

    result = dk.diff(
        old,
        pd.DataFrame(),
        verbosity=0,
        ).show().data  #type:ignore

    expected = pd.DataFrame({
        'diff': ['df removed'],
        'uid': ['x'],
        'value': [1],
        })

    assert_frame_equal(result, expected)
