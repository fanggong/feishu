import asyncio
from typing import Callable


async def run_in_back(sync_func: Callable, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: sync_func(**kwargs))
