import asyncio

# async keyword defines this as a coroutine. As such it can call await on some func or
# to yield control back to the event loop so it can execute another task
#


async def count(id):
    print(f"func_id:{id}, One")
    # give another func or task to run. That is, yield control to the event loop
    await asyncio.sleep(1)
    print(f"func_id:{id}, two")


async def main():
    await asyncio.gather(count("func-1"), count("func-2"), count('func-3'))

if __name__ == '__main__':
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() -s
    print(f"{__file__} executed in {elapsed:0.2f} seconds")