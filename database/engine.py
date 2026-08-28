from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///orion.db"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from database.models.task import Base

DATABASE_URL = "sqlite+aiosqlite:///orion.db"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
