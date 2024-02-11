import asyncio
import sys

from aiohttp import InvalidURL
from sqlalchemy.exc import IntegrityError

from OLDBASE_transfer.script import transfer
from logic import rec_link
from logic import update_path_parents, update_items_in_datadir
from engine import db
from logger import logger
from models import Base


async def main():
    print('If you want to parse the entire site, press "1", if you want to parse a separate link, then press "2"')
    print('Press "3" to migrate ONE item from OLD BASE')
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.create_all)
    try:
        choice = int(input())
        if choice == 1:
            print('Create directories (if necessary)')
            await update_path_parents()  # sync paths from path_links.txt and nanoreview
            await update_items_in_datadir()  # sync new items from DataBase and nanoreview
            # await add_all_items()  # add new items in DataBase
            logger.debug('Done. no errors')
            sys.exit('Success. Script stopped')
        if choice == 2:
            print('Past link FORMAT: https://nanoreview.net/ru/phone/..... now:')
            # Example: https://nanoreview.net/ru/phone/samsung-galaxy-m54
            try:
                link = str(input())
                await rec_link(link, to_path=True)
                print('Done')
            except IntegrityError:
                logger.debug('This element is already in the database')
            except InvalidURL as error:
                logger.debug('Error! Invalid Link:', error)
        if choice == 3:
            try:
                await transfer()
            except IndexError:
                logger.debug('Invalid title in OLD BASE')
        else:
            logger.debug('Incorrect input, you must press "1" or "2"\nExit')
    except BaseException as error:
        logger.debug(error)
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
