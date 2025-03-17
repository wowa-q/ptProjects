# PYTEST [pytest](https://pytest.org/en/latest/contents.html)

Unit test framework

To run the tests `pytest test_file.py`

## Use Cases

1. parametrize the test - the test will be executed 3 times

```python
V1 = Vector2D(0, 0)
V2 = Vector2D(-1, 1)
V3 = Vector2D(2.5, -2.5)

@pytest.mark.parametrize(
    ('lhs', 'rhs', 'exp_res'),
    (
        (V1, V2, Vector2D(-1, 1)),
        (V1, V3, Vector2D(2.5, -2.5)),
        (V3, V2, Vector2D(1.5, -1.5)),
    )
)

def test_add(lhs: Vector2D, rhs: Vector2D, exp_res: Vector2D) -> None:
    assert lhs + rhs == exp_res
```

1. skip the test: `@pytest.mark.skip(reason="not implemented")`
2. Test the function under test can raise an exception correctly

```python
@pytest.mark.parametrize(
    ('x', 'y'),
    (
        (None, -1),
        (0, None),
    )
)
def test_raises(x: Any, y: Any) -> None:
    with pytest.raises(TypeError):
        _ = Vector2D(x, y)
```