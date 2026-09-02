from datetime import datetime

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