import asyncio

queue = asyncio.Queue()
vip_queue = asyncio.Queue()

async def worker():
    while True:
        if not vip_queue.empty():
            task = await vip_queue.get()
            await task()
            vip_queue.task_done()
        else:
            task = await queue.get()
            await task()
            queue.task_done()

async def start_workers():
    for _ in range(7):
        asyncio.create_task(worker())
