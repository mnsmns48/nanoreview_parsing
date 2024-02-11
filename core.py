from typing import Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import DataDirectory, Main, Display, Performance, Camera, Energy, Communication, PhysicalParameters


async def add_path_data(session: AsyncSession, data: list):
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


async def get_items_by_code(session: AsyncSession, code: int):
    query = select(DataDirectory.title).filter(DataDirectory.parent == code)
    result: Result = await session.execute(query)
    return result.scalars().all()


async def get_links_by_code(session: AsyncSession, code: int):
    subq = select(Main.title).filter(DataDirectory.parent == code).scalar_subquery()
    query = select(DataDirectory).filter(and_(DataDirectory.title.not_in(subq)), (DataDirectory.parent == code))
    result: Result = await session.execute(query)
    return result.scalars().all()


async def add_one_link(session: AsyncSession, data: dict):
    await session.execute(Main.__table__.insert(), data.get('main'))
    await session.execute(Display.__table__.insert(), data.get('display'))
    await session.execute(Performance.__table__.insert(), data.get('performance'))
    await session.execute(Camera.__table__.insert(), data.get('camera'))
    await session.execute(Energy.__table__.insert(), data.get('energy'))
    await session.execute(Communication.__table__.insert(), data.get('communication'))
    await session.execute(PhysicalParameters.__table__.insert(), data.get('physicalparameters'))
    await session.commit()
