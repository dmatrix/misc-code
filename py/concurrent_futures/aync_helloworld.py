import asyncio


async def count(i):
    print(f"One: {i} count({i}) call")
    await asyncio.sleep(1)
    print(f"two: {i} count({i}) call")


async def main():

    # Create three function calls as part of the event loop
    await asyncio.gather(count(1), count(2), count(3))


if __name__ == '__main__':
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")