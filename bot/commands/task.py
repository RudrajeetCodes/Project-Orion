import discord
from database.session import SessionLocal
from discord import app_commands
from services.task_service import create_task


class TaskGroup(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="task",
            description="Manage your tasks",
        )

    @app_commands.command(
        name="add",
        description="Add a new task",
    )
    @app_commands.describe(title="The task you want to add")
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
    ):
        async with SessionLocal() as session:
            task = await create_task(session, title)

        await interaction.response.send_message(
            f"✅ Task #{task.id} created: **{task.title}**"
        )


task_group = TaskGroup()
