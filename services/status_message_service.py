from config import status_channel_id


STATUS_MARKER = "ORION_STATUS"


async def get_status_channel(client):
    channel = client.get_channel(status_channel_id)

    if channel is None:
        channel = await client.fetch_channel(status_channel_id)

    return channel


async def get_or_create_status_message(client):
    channel = await get_status_channel(client)

    async for message in channel.history(limit=50):
        if message.author == client.user and STATUS_MARKER in message.content:
            return message

    return await channel.send(STATUS_MARKER)