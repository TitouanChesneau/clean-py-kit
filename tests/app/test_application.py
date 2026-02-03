from cleanpykit.app import Application

def test_application_hooks_called():
    called = {"start": False, "stop": False}

    app = Application()

    app.on_startup(lambda: called.__setitem__("start", True))
    app.on_shutdown(lambda: called.__setitem__("stop", True))

    app.run(lambda: None)

    assert called["start"]
    assert called["stop"]

def test_application_crash_handling():
    called = {"start": False, "stop": False, "main": False}

    app = Application()

    app.on_startup(lambda: called.__setitem__("start", True))
    app.on_shutdown(lambda: called.__setitem__("stop", True))

    def main():
        called["main"] = True
        raise RuntimeError("Test exception")

    try:
        app.run(main)
    except RuntimeError:
        pass

    assert called["start"]
    assert called["main"]
    assert called["stop"]