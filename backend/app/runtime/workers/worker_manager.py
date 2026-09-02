import asyncio

async def start_worker():
    while True:
        print("AI worker runtime active...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(start_worker())