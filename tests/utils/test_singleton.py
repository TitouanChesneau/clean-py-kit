from pybase.utils import singleton

@singleton
class SingletonExample:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

def test_singleton_behavior():
    instance1 = SingletonExample()
    instance2 = SingletonExample()
    assert instance1 is instance2, "Singleton instances are not the same"

    initial_value = instance1.value
    instance1.increment()
    assert instance2.value == initial_value + 1, "Singleton state is not shared"

    instance2.increment()
    assert instance1.value == initial_value + 2, "Singleton state is not shared after second increment"
