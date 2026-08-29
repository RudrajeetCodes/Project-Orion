import discord
from config import guild_id
from discord import app_commands

from bot.commands.task import task_group


class OrionClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def setup_hook(self):
        guild = discord.Object(id=int(guild_id))

        # Remove any old global /task command.
        self.tree.remove_command("task")

        # Sync global commands.
        await self.tree.sync()

        # Add /task only to our development server.
        self.tree.add_command(task_group, guild=guild)

        # Sync guild commands.
        await self.tree.sync(guild=guild)

        print("Slash commands synced")


client = OrionClient()


@client.tree.command(name="ping", description="Check if Orion is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")
