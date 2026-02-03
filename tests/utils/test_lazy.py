from cleanpykit.utils import lazy

def test_lazy_called_once():
    class A:
        calls = 0

        @lazy
        def x(self):
            self.calls += 1
            return 42

    a = A()
    assert a.x == 42
    assert a.x == 42
    assert a.calls == 1


def test_lazy_different_instances():
    class A:
        calls = 0

        @lazy
        def x(self):
            self.calls += 1
            return 42

    a1 = A()
    a2 = A()
    assert a1.x == 42
    assert a2.x == 42
    assert a1.calls == 1
    assert a2.calls == 1

def test_lazy_no_instance():
    class A:
        @lazy
        def x(self):
            return 42

    assert A.x.__get__(None, A) is A.x