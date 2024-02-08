import asyncio
from bs import update_path_parents, update_all_items
from core import get_parent_code, add_data, check_title, get_all_paths
from engine import db
from logger import logger
from models import Base


async def full_scrape():
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    await update_path_parents()
    await update_all_items()
    # for path_name in path_names:
    #     async with db.scoped_session() as session:
    #         check = await check_title(session=session, title=path_name.get('title'))
    #         if check:
    #             logger.debug(f"{path_name.get('title')} is in the database")
    #         else:
    #             await add_data(session=session, data=path_name)
    #             logger.debug(f"{path_name.get('title')} is add to database")
    # async with db.scoped_session() as session:
    #     parents = await get_parent(session=session)
    # print(parents)

        # async with db.scoped_session() as session:
        #     await add_data(session=session, data=path_names)

        # for line in parents:
        #     await asyncio.sleep(1)
        #     ins_data = await get_links_in_path(code=int(line.code),
        #                                        link=line.link)
        #     async with db.scoped_session() as session:
        #         await add_data(session=session, data=ins_data)
        #     await asyncio.sleep(2)
        # async with db.scoped_session() as session:
        #     title = await check_title(session=session, title='Каталог смартфонов Motorola')
        # print(title)
