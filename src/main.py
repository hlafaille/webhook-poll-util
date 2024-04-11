from asyncio import Task, TaskGroup
import asyncio
from handler.configured_handler import ConfiguredHandler
from handler.introspect import get_handler_paths
from util import log

async def main():
    """Entry point
    """
    l = await log.get_logger("main")
    l.info("starting up")
    
    # load the handlers
    handler_paths = await get_handler_paths()
    tasks: list[Task] = [] # type: ignore
    for path in handler_paths:
        async with TaskGroup() as tg:
            tasks.append(tg.create_task(ConfiguredHandler.build(path))) # type: ignore
    
    # deal with tg results
    configured_handlers: list[ConfiguredHandler] = []
    for task in tasks: # type: ignore
        configured_handlers.append(task.result()) # type: ignore
    
    # enter the server loop
    while True:
        # iterate over handlers, determine which ones need re-polling.
        for handler in configured_handlers:
            
            


if __name__ == "__main__":
    asyncio.run(main())
