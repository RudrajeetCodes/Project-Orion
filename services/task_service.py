from database.models.task import Task
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(
    session: AsyncSession,
    title: str,
) -> Task:
    task = Task(title=title)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task
