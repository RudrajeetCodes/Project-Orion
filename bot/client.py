import discord


class OrionClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")


intents = discord.Intents.default()

client = OrionClient(intents=intents)
