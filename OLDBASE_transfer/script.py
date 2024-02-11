import asyncio

from pydantic_settings import BaseSettings
from sqlalchemy import select, Result, Table
from sqlalchemy.ext.asyncio import AsyncSession

from OLDBASE_transfer.old_models import s_main, display, performance, camera, communication, energy, \
    physical_parameters
from config import hidden
from core import add_one_link, add_path_data
from engine import DataBase, db
from support_func import change_key


class Settings(BaseSettings):
    db_url: str = (f"postgresql+asyncpg://{hidden.db_username}:{hidden.db_password}"
                   f"@localhost:{hidden.db_local_port}/{hidden.old_db}")
    db_echo: bool = False


settings_old_db = Settings()

old_db = DataBase(url=settings_old_db.db_url, echo=settings_old_db.db_echo)


async def get_old_info(session: AsyncSession, title: str):
    tables: list[Table] = [s_main, display, camera, performance, communication, energy, physical_parameters]
    result_dict = dict()
    for table in tables:
        query = select(table).filter(table.c.title == title)
        result: Result = await session.execute(query)
        result_dict.setdefault(change_key(table.name), {})
        for key, value in zip(result.keys(), result.all()[0]):
            result_dict[change_key(table.name)].update({change_key(key): value})
        await asyncio.sleep(0.1)
    return result_dict


async def transfer():
    print('Enter TITLE from the old database')
    title = str(input())
    async with old_db.scoped_session() as old_session:
        print('Checking....')
        data = await get_old_info(session=old_session, title=title)
    async with db.scoped_session() as session:
        await add_one_link(session=session, data=data)
    print('Done')


if __name__ == "__main__":
    asyncio.run(transfer())
