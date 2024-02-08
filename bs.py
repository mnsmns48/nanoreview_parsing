import asyncio
import random

import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import hidden
from core import get_all_paths, add_data, get_items, get_parent_code
from engine import db
from logger import logger

ua = UserAgent()


async def update_path_parents() -> None:
    result_list = list()
    async with db.scoped_session() as db_session:
        db_path_links = await get_all_paths(session=db_session)
        new_paths = list(set(hidden.links) - set(db_path_links))
        if len(new_paths) == 0:
            logger.debug(f"DataBase doesn't need updating")
            return None
        for path_link in new_paths:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as aiohttp_session:
                async with aiohttp_session.get(url=path_link,
                                               headers={
                                                   'User-Agent': ua.random
                                               },
                                               timeout=ClientTimeout(total=100)) as response:
                    text = await response.text()
                    html = BeautifulSoup(text, 'lxml')
            result = html.find('h1', class_='title-h1')
            result_list.append(
                {
                    'parent': 0,
                    'title': result.getText(),
                    'link': path_link
                }
            )
            logger.debug(f"{result.getText()} add to DataBase")
            await asyncio.sleep(random.randint(1, 4))
    if len(result_list) > 0:
        await add_data(session=db_session, data=result_list)
    else:
        logger.debug(f"DataBase PATH doesn't need updating")
        return None


async def update_all_items():
    result_list = list()
    async with db.scoped_session() as db_session:
        parent_codes = await get_parent_code(session=db_session)
    for code in parent_codes:
        async with db.scoped_session() as db_session:
            path_links = await get_all_paths(session=db_session)
        for link in path_links:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url=link,
                                       headers={
                                           'User-Agent': ua.random
                                       },
                                       timeout=ClientTimeout(total=100)) as response:
                    text = await response.text()
                    html = BeautifulSoup(text, 'lxml')
            result = html.find_all('a', style='font-weight:500;')
            res_dict = dict()
            for line in result:
                res_dict.update({line.getText(): line.get('href')})
                async with db.scoped_session() as db_session:
                    items_in_db = await get_items(session=db_session, code=code)
            new_items = list(set(res_dict.keys()) - set(items_in_db))
            if len(new_items) > 0:
                for key, value in res_dict.items():
                    result_list.append(
                        {
                            'parent': code,
                            'title': key,
                            'link': f"https://nanoreview.net{value}"
                        }
                    )
                    logger.debug(f"{key} add to DataBase")
                async with db.scoped_session() as db_session:
                    await add_data(session=db_session, data=result_list)
            else:
                logger.debug(f"DataBase ITEMS doesn't need updating")
            await asyncio.sleep(5)