import pytest
from database.models.task import Base, Task
from services.task_service import create_task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


@pytest.mark.asyncio
async def test_create_task():
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
        task = await create_task(
            session,
            "Finish probability assignment",
        )

        assert task.id is not None
        assert task.title == "Finish probability assignment"
        assert task.completed is False

        result = await session.execute(select(Task).where(Task.id == task.id))

        saved_task = result.scalar_one()

        assert saved_task.title == "Finish probability assignment"

    await engine.dispose()
