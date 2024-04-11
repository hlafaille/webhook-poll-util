import asyncio
from pathlib import Path
from handler.configured_handler import ConfiguredHandler
from util import log

async def main():
    """Entry point
    """
    l = await log.get_logger("main")
    l.info("starting up")
    
    await ConfiguredHandler.build(Path("handlers/x.py"))
    
    while True:
        pass


if __name__ == "__main__":
    asyncio.run(main())
