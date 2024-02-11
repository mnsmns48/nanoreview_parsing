import asyncio
import random

import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup

from bs import pars_link, ua
from config import hidden
from core import get_all_paths, add_path_data, get_parent_, get_items_by_code, add_one_link, get_links_by_code, \
    get_parent_by_title
from engine import db
from logger import logger


async def update_path_parents() -> None:
    result_list = list()
    async with db.scoped_session() as db_session:
        db_path_links = await get_all_paths(session=db_session)
        new_paths = list(set(hidden.links) - set(db_path_links))
        if len(new_paths) == 0:
            logger.debug(f"DataBase --PATH-- doesn't need updating")
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
        await add_path_data(session=db_session, data=result_list)
    else:
        logger.debug(f"DataBase --PATH-- doesn't need updating")
        return None


async def update_items_in_datadir():
    async with db.scoped_session() as db_session:
        parent_models = await get_parent_(session=db_session)
    for path in parent_models:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(url=path.link,
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
            items_in_db = await get_items_by_code(session=db_session, code=path.code)
        new_items = list(set(res_dict.keys()) - set(items_in_db))
        if len(new_items) > 0:
            result_list = list()
            for name in new_items:
                result_list.append(
                    {
                        'parent': path.code,
                        'title': name,
                        'link': f"https://nanoreview.net{res_dict.get(name)}"
                    }
                )
                logger.debug(f"<< {name} >> add to DataBase")
            async with db.scoped_session() as db_session:
                await add_path_data(session=db_session, data=result_list)
                result_list.clear()
        else:
            database_name = result[1].getText()
            logger.debug(f"DataBase << {database_name.split(' ')[0]} >> doesn't need updating")
        await asyncio.sleep(random.randint(2, 5))


async def rec_link(link: str, to_path: bool):
    item_data = await pars_link(link=link)
    async with db.scoped_session() as db_session:
        await add_one_link(session=db_session, data=item_data)
        if to_path:
            await add_path_data(session=db_session, data=[
                {
                    'parent': await get_parent_by_title(session=db_session, title=item_data.get('main')['title']),
                    'title': item_data.get('main')['title'],
                    'link': link
                }
            ]
                                )


async def add_all_items():
    async with db.scoped_session() as db_session:
        parent_models = await get_parent_(session=db_session)
        for line in parent_models:
            links_to_rec = await get_links_by_code(session=db_session, code=line.code)
            for link in links_to_rec:
                await rec_link(link.link, to_path=False)
                sek = random.randint(3, 5)
                logger.debug(f"{link.title} add to DataBase. I'm waiting {sek} sek")
                await asyncio.sleep(sek)
