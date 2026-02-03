from typing import Callable, List
from cleanpykit.logging import get_logger
from cleanpykit.di import Container

class Application:
    def __init__(self, container: Container | None = None):
        self.container = container or Container()
        self._startup_hooks: List[Callable[[], None]] = []
        self._shutdown_hooks: List[Callable[[], None]] = []
        self.logger = get_logger(self.__class__.__name__, level="INFO", use_color=True)
    
    def on_startup(self, hook: Callable[[], None]):
        """Register a function to run at startup"""
        self._startup_hooks.append(hook)
    
    def on_shutdown(self, hook: Callable[[], None]):
        """Register a function to run at shutdown"""
        self._shutdown_hooks.append(hook)

    def run(self, main: Callable[[], None]):
        """Run the application with startup an shutdown hooks"""
        try:
            self.logger.info("Application starting...")
            for hook in self._startup_hooks:
                hook()
            main()
        except Exception as e:
            self.logger.error("Unhandled exception occurred", exc_info=True)
            raise
        finally:
            self.logger.info("Application shuting down...")
            for hook in self._shutdown_hooks:
                hook()