from asyncio import get_event_loop
from .deps import app
from .config import get_config
from uvicorn import run


from .controller.note import *


async def start():
    config = get_config()
    run(app, host=config.http_host, port=config.http_port)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(start())
