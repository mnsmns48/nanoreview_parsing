import asyncio
import sys

from bs import pars_link
from logic import update_path_parents, update_items_in_datadir, add_all_items
from engine import db
from logger import logger
from models import Base


async def main():
    await pars_link('https://nanoreview.net/ru/phone/xiaomi-redmi-a2')
    # await add_all_items()
    # print('If you want to parse the entire site, press "1", if you want to parse a separate link, then press "2"')
    # try:
    #     choice = int(input())
    #     if choice == 1:
    #         async with db.engine.begin() as async_connect:
    #             await async_connect.run_sync(Base.metadata.create_all)
    #         await update_path_parents()
    #         await update_items_in_datadir()
    #         sys.exit('Success. Script stopped')
    #     if choice == 2:
    #         pass
    #         # await one_link()
    #     else:
    #         logger.debug('Incorrect input, you must press "1" or "2"\nExit')
    # except BaseException as error:
    #     logger.debug(error)
    # await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
