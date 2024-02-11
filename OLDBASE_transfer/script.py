import asyncio

from pydantic_settings import BaseSettings
from sqlalchemy import select, Result, and_
from sqlalchemy.ext.asyncio import AsyncSession

from OLDBASE_transfer.old_models import s_main, display, performance, camera, communication, energy, \
    physical_parameters
from config import hidden
from engine import DataBase


class Settings(BaseSettings):
    db_url: str = (f"postgresql+asyncpg://{hidden.db_username}:{hidden.db_password}"
                   f"@localhost:{hidden.db_local_port}/Phones")
    db_echo: bool = False


settings_old_db = Settings()

old_db = DataBase(url=settings_old_db.db_url, echo=settings_old_db.db_echo)


async def get_old_info(session: AsyncSession, title: str):
    query = select(s_main, display, camera, performance, communication, energy, physical_parameters) \
        .filter(and_(
                    (s_main.c.title == title),
                    (s_main.c.title == display.c.title),
                    (s_main.c.title == camera.c.title),
                    (s_main.c.title == performance.c.title),
                    (s_main.c.title == communication.c.title),
                    (s_main.c.title == energy.c.title),
                    (s_main.c.title == physical_parameters.c.title),
            )
    )
    result: Result = await session.execute(query)
    return result


async def transfer():
    # print('Введите название в старой БД')
    # title = str(input())
    # async with old_db.engine.begin() as async_connect:
    #     await async_connect.run_sync(metadata.create_all)
    async with old_db.scoped_session() as old_ses:
        data = await get_old_info(session=old_ses, title='TCL 30')
    dict_data = dict()
    for key, value in zip(data.keys(), data.all()[0]):
        dict_data.update({
            key: value
        })
    dict1[] = dict1.pop('old_key')


if __name__ == "__main__":
    asyncio.run(transfer())
