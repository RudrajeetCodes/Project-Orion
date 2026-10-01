import asyncio

import discord
from discord import app_commands

from bot.commands.reminder import reminder_group
from bot.commands.task import task_group
from config import guild_id
from services.status_message_service import (
    get_or_create_status_message,
    update_status,
)
from workers.reminder_worker import reminder_worker


class OrionClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def setup_hook(self):
        guild = discord.Object(id=int(guild_id))

        self.tree.remove_command("task")
        await self.tree.sync()

        self.tree.add_command(task_group, guild=guild)
        self.tree.add_command(reminder_group, guild=guild)
        await self.tree.sync(guild=guild)
        await update_status(self)

        asyncio.create_task(reminder_worker(self))

        print("Slash commands synced")


client = OrionClient()


@client.tree.command(name="ping", description="Check if Orion is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")
