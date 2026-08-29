from database.models.task import Task
from sqlalchemy import select
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


async def get_tasks(session: AsyncSession) -> list[Task]:
    result = await session.execute(select(Task).where(Task.completed.is_(False)))

    return list(result.scalars().all())


async def complete_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    task = await session.get(Task, task_id)

    if task is None:
        return None

    task.completed = True

    await session.commit()
    await session.refresh(task)

    return task


async def delete_task(
    session: AsyncSession,
    task_id: int,
) -> Task | None:
    task = await session.get(Task, task_id)

    if task is None:
        return None

    await session.delete(task)
    await session.commit()

    return task


async def edit_task(
    session: AsyncSession,
    task_id: int,
    new_title: str,
) -> Task | None:
    task = await session.get(Task, task_id)

    if task is None:
        return None

    task.title = new_title

    await session.commit()
    await session.refresh(task)

    return task
