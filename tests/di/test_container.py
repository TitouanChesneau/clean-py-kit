from pybase.di import Container

class A:
    pass

class B:
    a: A
    def __init__(self, a: A):
        self.a = a

def test_container_resolve():
    c = Container()
    c.bind(A)
    c.bind(B)

    b = c.resolve(B)
    assert isinstance(b.a, A)

def test_container_crash_on_unbound():
    c = Container()

    try:
        c.resolve(B)
        assert False, "Expected KeyError for unbound dependency"
    except KeyError:
        pass

def test_container_singleton_behavior():
    c = Container()
    c.bind(A)
    c.bind(B)

    b1 = c.resolve(B)
    b2 = c.resolve(B)

    assert b1 is b2
    assert b1.a is b2.a

def test_container_override():
    c = Container()
    c.bind(A)
    c.bind(B)

    a_instance = A()
    c.override(A, a_instance)

    b = c.resolve(B)
    assert b.a is a_instance

def test_container_override_clears_dependent_instances():
    c = Container()
    c.bind(A)
    c.bind(B)

    b1 = c.resolve(B)
    a_instance = A()
    c.override(A, a_instance)
    b2 = c.resolve(B)

    assert b1 is not b2
    assert b2.a is a_instance