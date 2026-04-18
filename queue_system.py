import asyncio

queue = asyncio.Queue()

async def worker():
    while True:
        task = await queue.get()
        await task()
        queue.task_done()
