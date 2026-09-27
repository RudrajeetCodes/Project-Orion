import os


from dotenv import load_dotenv

load_dotenv()



token = os.getenv("DISCORD_TOKEN")
guild_id = os.getenv("GUILD_ID")
owner_id = int(os.getenv("OWNER_ID"))
