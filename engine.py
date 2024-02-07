from pydantic.v1 import BaseSettings
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from config import hidden


class CoreConfig(BaseSettings):
    base: str = (
        f"postgresql+asyncpg://{hidden.db_username}:{hidden.db_password}"
        f"@localhost:{hidden.db_local_port}/{hidden.db_name}"
    )
    db_echo: bool = False


dbconfig = CoreConfig()
engine = create_async_engine(url=dbconfig.base,
                             echo=dbconfig.db_echo,
                             poolclass=NullPool)
