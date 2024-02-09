from typing import Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import DataDirectory


async def add_data(session: AsyncSession, data: list):
    stmt = insert(table=DataDirectory).values(data)
    await session.execute(stmt)
    await session.commit()


async def get_parent_(session: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    query = select(DataDirectory).filter(DataDirectory.parent == 0)
    parents: Result = await session.execute(query)
    return parents.scalars().all()


async def check_title(session: AsyncSession, title: str):
    query = select(DataDirectory.title).filter(DataDirectory.title == title)
    res_title: Result = await session.execute(query)
    return res_title.scalar()


async def get_all_paths(session: AsyncSession):
    query = select(DataDirectory.link).filter(DataDirectory.parent == 0)
    result: Result = await session.execute(query)
    return result.scalars().all()


async def get_items(session: AsyncSession, code: int):
    query = select(DataDirectory.title).filter(DataDirectory.parent == code)
    result: Result = await session.execute(query)
    return result.scalars().all()


async def get_links(session: AsyncSession, code: int):
    query = select(DataDirectory.link).filter(DataDirectory.parent == code)
    result: Result = await session.execute(query)
    return result.scalars().all()
