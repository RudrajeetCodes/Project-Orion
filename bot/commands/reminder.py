from datetime import datetime

import discord
from discord import app_commands

from database.session import SessionLocal
from services.reminder_service import (
    cancel_reminder,
    create_reminder,
    edit_reminder,
    get_reminders,
)


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

    @app_commands.command(
        name="list",
        description="List your reminders",
    )
    async def list_reminders(self, interaction: discord.Interaction):
        async with SessionLocal() as session:
            reminders = await get_reminders(session)

        if not reminders:
            await interaction.response.send_message("⏰ You have no reminders.")
            return

        lines = ["⏰ **Your Reminders**", ""]

        for reminder in reminders:
            remind_at = reminder.remind_at.strftime("%b %d at %I:%M %p")

            lines.append(f"{reminder.id}. ⏰ **{reminder.message}**\n   {remind_at}")

        await interaction.response.send_message("\n".join(lines))

    @app_commands.command(
        name="cancel",
        description="Cancel a reminder",
    )
    @app_commands.describe(
        reminder_id="The ID of the reminder to cancel",
    )
    async def cancel(
        self,
        interaction: discord.Interaction,
        reminder_id: int,
    ):
        async with SessionLocal() as session:
            reminder = await cancel_reminder(
                session,
                reminder_id,
            )

        if reminder is None:
            await interaction.response.send_message(
                f"❌ Reminder #{reminder_id} was not found."
            )
            return

        await interaction.response.send_message(
            f"🗑️ Cancelled reminder #{reminder.id}: **{reminder.message}**"
        )

    @app_commands.command(
        name="edit",
        description="Edit a reminder",
    )
    @app_commands.describe(
        reminder_id="The ID of the reminder to edit",
        message="The new reminder message",
        remind_at="The new reminder time: YYYY-MM-DD HH:MM",
    )
    async def edit(
        self,
        interaction: discord.Interaction,
        reminder_id: int,
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
            reminder = await edit_reminder(
                session,
                reminder_id,
                message,
                remind_at_dt,
            )

        if reminder is None:
            await interaction.response.send_message(
                f"❌ Reminder #{reminder_id} was not found."
            )
            return

        await interaction.response.send_message(
            f"✏️ Updated reminder #{reminder.id}: "
            f"**{reminder.message}** at "
            f"{reminder.remind_at.strftime('%b %d at %I:%M %p')}"
        )


reminder_group = ReminderGroup()
