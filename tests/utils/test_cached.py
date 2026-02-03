from cleanpykit.utils import cached

def test_cached_called_once():
    calls = {"n": 0}

    @cached
    def f(x):
        calls["n"] += 1
        return x * 2

    assert f(2) == 4
    assert f(2) == 4
    assert calls["n"] == 1