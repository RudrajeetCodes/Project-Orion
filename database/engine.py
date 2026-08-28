from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DATABASE_URL = "sqlite+aiosqlite:///orion.db"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)