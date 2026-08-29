from datetime import datetime

import discord
from database.session import SessionLocal
from discord import app_commands
from services.task_service import (
    complete_task,
    create_task,
    delete_task,
    edit_task,
    get_tasks,
)


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
    @app_commands.describe(
        title="The task you want to add",
        priority="Task priority",
        due="Due date: YYYY-MM-DD HH:MM",
    )
    @app_commands.choices(
        priority=[
            app_commands.Choice(name="Low", value="low"),
            app_commands.Choice(name="Normal", value="normal"),
            app_commands.Choice(name="High", value="high"),
        ]
    )
    async def add(
        self,
        interaction: discord.Interaction,
        title: str,
        priority: app_commands.Choice[str],
        due: str | None = None,
    ):
        due_at = None

        if due:
            try:
                due_at = datetime.strptime(due, "%Y-%m-%d %H:%M")
            except ValueError:
                await interaction.response.send_message(
                    "❌ Invalid date format. Use `YYYY-MM-DD HH:MM`."
                )
                return

        async with SessionLocal() as session:
            task = await create_task(
                session,
                title,
                priority.value,
                due_at,
            )

        await interaction.response.send_message(
            f"✅ Task #{task.id} created: **{task.title}**"
        )

    @app_commands.command(
        name="list",
        description="List your incomplete tasks",
    )
    async def list_tasks(self, interaction: discord.Interaction):
        async with SessionLocal() as session:
            tasks = await get_tasks(session)

        if not tasks:
            await interaction.response.send_message("🎉 You have no incomplete tasks!")
            return

        lines = ["📋 **Your Tasks**", ""]

        for task in tasks:
            priority = task.priority.capitalize()

            if task.due_at:
                due = task.due_at.strftime("%b %d at %I:%M %p")
            else:
                due = "No due date"

            lines.append(f"{task.id}. ⬜ **{task.title}**\n   {priority} · {due}")

        await interaction.response.send_message("\n".join(lines))

    @app_commands.command(
        name="complete",
        description="Mark a task as completed",
    )
    @app_commands.describe(task_id="The ID of the task to complete")
    async def complete(
        self,
        interaction: discord.Interaction,
        task_id: int,
    ):
        async with SessionLocal() as session:
            task = await complete_task(session, task_id)

        if task is None:
            await interaction.response.send_message(
                f"❌ Task #{task_id} was not found."
            )
            return

        await interaction.response.send_message(
            f"✅ Completed task #{task.id}: **{task.title}**"
        )

    @app_commands.command(
        name="delete",
        description="Delete a task",
    )
    @app_commands.describe(task_id="The ID of the task to delete")
    async def delete(
        self,
        interaction: discord.Interaction,
        task_id: int,
    ):
        async with SessionLocal() as session:
            task = await delete_task(session, task_id)

        if task is None:
            await interaction.response.send_message(
                f"❌ Task #{task_id} was not found."
            )
            return

        await interaction.response.send_message(
            f"🗑️ Deleted task #{task.id}: **{task.title}**"
        )

    @app_commands.command(
        name="edit",
        description="Edit a task's title",
    )
    @app_commands.describe(
        task_id="The ID of the task to edit",
        title="The new task title",
    )
    async def edit(
        self,
        interaction: discord.Interaction,
        task_id: int,
        title: str,
    ):
        async with SessionLocal() as session:
            task = await edit_task(session, task_id, title)

        if task is None:
            await interaction.response.send_message(
                f"❌ Task #{task_id} was not found."
            )
            return

        await interaction.response.send_message(
            f"✏️ Updated task #{task.id}: **{task.title}**"
        )


task_group = TaskGroup()
