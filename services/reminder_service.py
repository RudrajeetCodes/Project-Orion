from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.reminder import Reminder


async def create_reminder(
    session: AsyncSession,
    message: str,
    remind_at: datetime,
) -> Reminder:
    reminder = Reminder(
        message=message,
        remind_at=remind_at,
    )

    session.add(reminder)
    await session.commit()
    await session.refresh(reminder)

    return reminder


async def get_reminders(
    session: AsyncSession,
) -> list[Reminder]:
    result = await session.execute(select(Reminder).order_by(Reminder.remind_at))

    return list(result.scalars().all())


async def cancel_reminder(
    session: AsyncSession,
    reminder_id: int,
) -> Reminder | None:
    reminder = await session.get(Reminder, reminder_id)

    if reminder is None:
        return None

    await session.delete(reminder)
    await session.commit()

    return reminder
