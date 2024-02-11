import asyncio
import sys

from aiohttp import InvalidURL

from logic import rec_link, add_all_items
from logic import update_path_parents, update_items_in_datadir
from engine import db
from logger import logger
from models import Base


async def main():
    print('If you want to parse the entire site, press "1", if you want to parse a separate link, then press "2"')
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    try:
        choice = int(input())
        if choice == 1:
            print('Create directories (if necessary)')
            await update_path_parents()
            await update_items_in_datadir()
            await add_all_items()
            logger.debug('Done. no errors')
            sys.exit('Success. Script stopped')
        if choice == 2:
            print('Past link FORMAT: https://nanoreview.net/ru/phone/..... now:')
            try:
                link = str(input())
                await rec_link(link)
                print('Done')
            except InvalidURL as error:
                logger.debug('Error! Invalid Link:', error)
        else:
            logger.debug('Incorrect input, you must press "1" or "2"\nExit')
    except BaseException as error:
        logger.debug(error)
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
