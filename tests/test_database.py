import pytest
from database.models.task import Base, Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.mark.asyncio
async def test_create_and_read_task():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with SessionLocal() as session:
        task = Task(title="Learn SQLAlchemy")

        session.add(task)
        await session.commit()

        result = await session.execute(
            select(Task).where(Task.title == "Learn SQLAlchemy")
        )

        saved_task = result.scalar_one()

        assert saved_task.title == "Learn SQLAlchemy"
        assert saved_task.completed is False

    await engine.dispose()
