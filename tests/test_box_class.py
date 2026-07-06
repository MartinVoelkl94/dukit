
import pytest
from dukit import Box



params = [
    ({'a': 3}, 3),
    ({'x': 'y'}, 'y'),
    ]
@pytest.mark.parametrize('kwargs, expected_attr', params)
def test_basics(kwargs, expected_attr):
    box = Box(**kwargs)
    key = list(kwargs.keys())[0]
    assert box[key] == expected_attr



def test_copy_clear_new():
    box = Box(a=1)
    assert box.a == 1  #type: ignore
    assert box['a'] == 1

    box_copy = box.copy()
    assert box_copy == box

    box_new = box.new(b=2)
    assert box_new.b == 2  #type: ignore
    assert box_new['b'] == 2
    assert hasattr(box_new, 'a') is False
    assert 'a' not in box_new.keys()

    box.clear()
    assert hasattr(box, 'b') is False
    assert 'b' not in box.keys()
    assert dict(box.items()) == {}



params = [
    (1.5, 'x', TypeError),
    (object(), None, TypeError),
    ('keys', 1, AttributeError),
    ]
@pytest.mark.parametrize('name, value, error_type', params)
def test_setattr_errors(name, value, error_type):
    box = Box()
    with pytest.raises(error_type):
        setattr(box, name, value)



params = [
    (1.5, KeyError),
    (object(), KeyError),
    ]
@pytest.mark.parametrize('key, error_type', params)
def test_getitem_errors(key, error_type):
    box = Box()
    with pytest.raises(error_type):
        _ = box[key]



def test_repr_str_print_eq():
    box = Box(a=1)
    text = str(box)
    assert 'Box(' in text
    assert '<Box;' in repr(box)

    box.print()

    assert (box == Box(a=1)) is True
    assert (box == 'x') is False
