from datetime import datetime

import discord
from discord import app_commands

from database.session import SessionLocal
from services.reminder_service import create_reminder


class ReminderGroup(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="remind",
            description="Manage your reminders",
        )

    @app_commands.command(
        name="add",
        description="Add a reminder",
    )
    @app_commands.describe(
        message="What you want to be reminded about",
        remind_at="Reminder time: YYYY-MM-DD HH:MM",
    )
    async def add(
        self,
        interaction: discord.Interaction,
        message: str,
        remind_at: str,
    ):
        try:
            remind_at_dt = datetime.strptime(
                remind_at,
                "%Y-%m-%d %H:%M",
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid date format. Use `YYYY-MM-DD HH:MM`."
            )
            return

        async with SessionLocal() as session:
            reminder = await create_reminder(
                session,
                message,
                remind_at_dt,
            )

        await interaction.response.send_message(
            f"⏰ Reminder #{reminder.id} created: "
            f"**{reminder.message}** at "
            f"{reminder.remind_at.strftime('%b %d at %I:%M %p')}"
        )


reminder_group = ReminderGroup()
