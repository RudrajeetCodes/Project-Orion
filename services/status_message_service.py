from config import status_channel_id, status_message_id
from database.session import SessionLocal
from services.status_service import build_status


async def get_status_channel(client):
    channel = client.get_channel(status_channel_id)

    if channel is None:
        channel = await client.fetch_channel(status_channel_id)

    return channel


async def get_or_create_status_message(client):
    channel = await get_status_channel(client)

    if status_message_id:
        return await channel.fetch_message(int(status_message_id))

    return await channel.send("ORION_STATUS")


async def update_status(client):
    message = await get_or_create_status_message(client)

    async with SessionLocal() as session:
        status = await build_status(session)

    await message.edit(content=status)