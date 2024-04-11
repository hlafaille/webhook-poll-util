import datetime
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
    _last_poll: datetime.datetime | None

    def __init__(self, name: str, path: Path, log: logging.Logger) -> None:
        self._name = name
        self._path = path
        self._log = log
        self._last_poll = None

    @classmethod
    async def build(cls, path: Path) -> "ConfiguredHandler":
        """Asynchronously construct a `ConfiguredHandler`.

        Args:
            path (Path): Filesystem path to the handler
        """
        handler_name = await fs.handler_name_from_path(path)
        instance = cls(
            handler_name, path, await log.get_logger(f"handler:{handler_name}")
        )
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
            raise HandlerMissingAttributeException(
                handler_name=self._name, attribute_name=e.name
            )

        self._log.info(f"loaded handler")

    async def poll(self):
        """Helper for calling the `poll()` function for this handler."""
        await self._poll()
        self._last_poll = datetime.datetime.now(datetime.UTC)

    async def is_ready_for_polling(self) -> bool:
        """If this handler is ready for polling again. This checks for if
        `last time polled + interval in ms` is `>=` the current time.

        Returns:
            bool: True if ready for polling, False if not.
        """
