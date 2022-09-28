import random
import logging
import time
import os
import asyncio
import aiohttp
import aiofiles
from aiohttp_requests import requests

import ray

FLAGS = ['CN', 'IN', 'US', 'ID', 'BR', 'PK', 'NG', 'BD', 'JP', 'MX', 'PH', 'VN', 'ET', 'EG', 'DE', 'IR', 'TR', 'CD', 'FR', 'GR']
FLAGS_URL = "http://flupy.org/data/flags"
BASE_DIR = "./downloads"

async def main(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image = await resp.content
            return image

@ray.remote
class AsyncFlagActor:

    async def run_tasks(self, cc, verbose):
        if verbose:
            print(f"Started task-id='{cc}'")
        result = await self.do_task(cc)
        if verbose:
            print(f"finished task=i='{cc}'")
        return result

    async def do_task(self, flag):
        file_name = f"{flag.lower()}.gif"
        url = f"{FLAGS_URL}/{file_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                path = os.path.join(BASE_DIR, file_name)
                f = await aiofiles.open(path, mode='wb')
                await f.write(await resp.read())
                await f.close()
        return flag
        
if __name__ == "__main__":

    if ray.is_initialized:
        ray.shutdown()
    ray.init(logging_level=logging.ERROR)

    verbose = False
    start = time.time()
    async_actor= AsyncFlagActor.options(max_concurrency=len(FLAGS)).remote()
    results = ray.get([async_actor.run_tasks.remote(cc, verbose) for cc in FLAGS])
    print(f"AsyncFlagActor: Time elapsed:{time.time() - start:.2f}")
    print(results)