import asyncio

from engine import engine
from models import Base


async def full_scrape():
    async with engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
