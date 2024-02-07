import asyncio
import sys

from core import full_scrape
from logger import logger


async def main():
    print('If you want to parse the entire site, press "1", if you want to parse a separate link, then press "2"')
    try:
        choice = int(input())
        if choice == 1:
            await full_scrape()
            sys.exit('Success. Script stopped')
        if choice == 2:
            pass
            # await one_link()
        else:
            logger.debug('Incorrect input, you must press "1" or "2"\nExit')
    except BaseException as e:
        logger.debug(e)
    await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
