import asyncio

from bot.client import client
from config import token
from database.engine import init_db


async def startup() -> None:
    await init_db()


if __name__ == "__main__":
    asyncio.run(startup())
    client.run(token)
