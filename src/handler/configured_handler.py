import datetime
import importlib
import logging
from pathlib import Path
from types import ModuleType
from typing import Callable, Coroutine
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
    _poll: Callable[[], Coroutine[None, None, PollResponseContext]]
    _build_webhook_payload_context: Callable[[], JsonWebhookPayloadContext]
    _last_poll: datetime.datetime | None
    _last_poll_response_context: PollResponseContext | None

    def __init__(self, name: str, path: Path, log: logging.Logger) -> None:
        self._name = name
        self._path = path
        self._log = log
        self._last_poll = None

    @classmethod
    def build(cls, path: Path) -> "ConfiguredHandler":
        """Construct a `ConfiguredHandler`.

        Args:
            path (Path): Filesystem path to the handler
        """
        handler_name = fs.handler_name_from_path(path)
        instance = cls(handler_name, path, log.get_logger(f"handler:{handler_name}"))
        instance._parse()
        return instance

    def _parse(self) -> None:
        """Parse the Python file at _path. This `ConfiguredHandler` will expose method API to interact with the handler."""
        # load the module (must be in PYTHONPATH!)
        package, module = fs.path_to_import_notation(self._path)
        self._module = importlib.import_module(name=module, package=package)

        try:
            self._interval = self._module.INTERVAL
            self._poll = self._module.poll
            self._build_webhook_context = self._module.build_webhook_payload_context
        except AttributeError as e:
            raise HandlerMissingAttributeException(
                handler_name=self._name, attribute_name=e.name
            )

        self._log.info(f"loaded handler")

    async def do(self):
        """Polls the handler, handles calling the webhook with the built payload context."""
        try:
            self._last_poll_response_context = await self._poll()
        except Exception as e:
            self._log.exception(
                msg="exception occurred within configured handler, setting poll response context to unhealthy",
                exc_info=e,
            )
            self._last_poll_response_context = PollResponseContext(
                is_healthy=False,
                pretty_message="Exception occurred during polling of handler",
            )
        self._last_poll = datetime.datetime.now(datetime.UTC)
        await self.handle_poll_response()

    async def handle_poll_response(self):
        """Handle the poll's response. This involves sending the webhook call.

        Args:
            poll_response (PollResponseContext): _description_
        """

    def needs_polling(self) -> bool:
        """If this handler is ready for polling again. This checks for if
        `last time polled + interval in ms` is `>=` the current time.

        Returns:
            bool: True if ready for polling, False if not.
        """
        if self._last_poll == None:
            return True
        if datetime.datetime.now(datetime.UTC) > self._last_poll + datetime.timedelta(
            milliseconds=self._interval
        ):
            return True
        return False
