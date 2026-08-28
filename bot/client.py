import discord
from discord import app_commands


class OrionClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced")


client = OrionClient()


@client.tree.command(name="ping", description="Check if Orion is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")
