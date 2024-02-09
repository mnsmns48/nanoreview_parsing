import asyncio
from bs import update_path_parents, update_all_items
from core import add_data, check_title, get_all_paths
from engine import db
from logger import logger
from models import Base


async def full_scrape():
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    await update_path_parents()
    await update_all_items()
