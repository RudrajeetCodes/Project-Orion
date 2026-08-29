from datetime import datetime

from database.models.task import Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(
    session: AsyncSession,
    title: str,
    priority: str = "normal",
    due_at: datetime | None = None,
) -> Task:
    task = Task(
        title=title,
        priority=priority,
        due_at=due_at,
    )

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


async def get_tasks_due_today(
    session: AsyncSession,
    start: datetime,
    end: datetime,
) -> list[Task]:
    result = await session.execute(
        select(Task)
        .where(
            Task.completed.is_(False),
            Task.due_at >= start,
            Task.due_at < end,
        )
        .order_by(Task.due_at)
    )

    return list(result.scalars().all())


async def get_overdue_tasks(
    session: AsyncSession,
    now: datetime,
) -> list[Task]:
    result = await session.execute(
        select(Task)
        .where(
            Task.completed.is_(False),
            Task.due_at < now,
        )
        .order_by(Task.due_at)
    )

    return list(result.scalars().all())


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
