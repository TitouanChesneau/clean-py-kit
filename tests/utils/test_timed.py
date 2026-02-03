from pybase.utils import timed

class DummyLogger:
    def __init__(self):
        self.called = False

    def info(self, msg, extra=None):
        self.called = True
        assert "executed in" in msg
        assert "duration" in extra

def test_timed_logs():
    logger = DummyLogger()

    @timed(logger=logger)
    def f():
        return 1

    assert f() == 1
    assert logger.called

def test_timed_no_logger():
    @timed()
    def f():
        return 2

    assert f() == 2

import asyncio
def test_timed_async_logs():
    logger = DummyLogger()

    @timed(logger=logger)
    async def f():
        await asyncio.sleep(0.01)
        return 3

    result = asyncio.run(f())
    assert result == 3
    assert logger.called