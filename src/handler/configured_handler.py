import importlib
import logging
from pathlib import Path
from types import ModuleType
from typing import Callable
from exception import HandlerMissingAttributeException
from handler.context import JsonWebhookPayloadContext, PollResponseContext
from util import fs, log

class ConfiguredHandler:
    """A handler within the defined handler directory"""

    _name: str
    _path: Path
    _log: logging.Logger
    _module: ModuleType
    _interval: int
    _poll: Callable[[], PollResponseContext]
    _build_webhook_context: Callable[[PollResponseContext], JsonWebhookPayloadContext]
    
    def __init__(self, name: str, path: Path, log: logging.Logger) -> None:
        self._name = name
        self._path = path
        self._log = log

    @classmethod
    async def build(cls, path: Path) -> "ConfiguredHandler":
        """Asynchronously construct a `ConfiguredHandler`.

        Args:
            path (Path): Filesystem path to the handler
        """
        handler_name = await fs.handler_name_from_path(path)
        instance = cls(handler_name, path, await log.get_logger(f"handler:{handler_name}"))
        await instance._parse()
        return instance

    async def _parse(self) -> None:
        """Parse the Python file at _path. This `ConfiguredHandler` will expose method API to interact with the handler."""
        # load the module (must be in PYTHONPATH!)
        package, module = await fs.path_to_import_notation(self._path)
        self._module = importlib.import_module(name=module, package=package)
        
        try:
            self._interval = self._module.INTERVAL
            self._poll = self._module.poll
            self._build_webhook_context = self._module.build_webhook_context
        except AttributeError as e:
            raise HandlerMissingAttributeException(handler_name=self._name, attribute_name=e.name)
        
        self._log.info(f"loaded handler")
    
    async def poll(self):
        """Call the `poll()` function for this handler.
        """
        self._poll()
