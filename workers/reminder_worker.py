import asyncio
from datetime import datetime

from config import owner_id
from database.session import SessionLocal
from services.reminder_service import (
    get_due_reminders,
    mark_reminder_sent,
)


async def reminder_worker(client):
    while True:
        now = datetime.now()

        async with SessionLocal() as session:
            reminders = await get_due_reminders(session, now)

            for reminder in reminders:
                print(f"Processing reminder #{reminder.id}: {reminder.message}")

                user = await client.fetch_user(owner_id)

                await user.send(
                    f"⏰ **Reminder**\n{reminder.message}"
                )

                await mark_reminder_sent(session, reminder.id)

        await asyncio.sleep(10)