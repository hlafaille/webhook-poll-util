import asyncio
from handler.configured_handler import ConfiguredHandler
from handler.introspect import get_handler_paths
from util import log


async def main() -> int:
    """Entry point"""
    l = log.get_logger("main")
    l.info("starting up")

    # load the handlers
    handler_paths = get_handler_paths()
    configured_handlers: list[ConfiguredHandler] = []
    for path in handler_paths:
        configured_handlers.append(ConfiguredHandler.build(path))
    
    # enter the server loop, only exiting if exit_code becomes an int
    exit_code: int | None = None
    while exit_code == None:
        # poll the handlers that need polling
        for handler in [x for x in configured_handlers if x.needs_polling()]:
            await handler.do()
            
    return exit_code

if __name__ == "__main__":
    exit(asyncio.run(main()))
