from datetime import datetime, time, timedelta

import discord
from discord import app_commands

from database.session import SessionLocal
from services.task_service import (
    clear_completed_tasks,
    complete_task,
    create_task,
    delete_task,
    edit_task,
    get_overdue_tasks,
    get_tasks,
    get_tasks_due_today,
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
            await interaction.response.send_message("🎉 You have no tasks!")
            return

        lines = ["📋 **Your Tasks**", ""]

        for task in tasks:
            priority = task.priority.capitalize()

            if task.due_at:
                due = task.due_at.strftime("%b %d at %I:%M %p")
            else:
                due = "No due date"

            status = "✅" if task.completed else "⬜"

            lines.append(f"{task.id}. {status} **{task.title}**\n   {priority} · {due}")

        await interaction.response.send_message("\n".join(lines))

    @app_commands.command(
        name="overdue",
        description="Show overdue tasks",
    )
    async def overdue(self, interaction: discord.Interaction):
        await interaction.response.defer()

        now = datetime.now()

        async with SessionLocal() as session:
            tasks = await get_overdue_tasks(
                session,
                now,
            )

        if not tasks:
            await interaction.followup.send("🎉 You have no overdue tasks!")
            return

        lines = ["🚨 **Overdue Tasks**", ""]

        for task in tasks:
            priority = task.priority.capitalize()
            due = task.due_at.strftime("%b %d at %I:%M %p")

            lines.append(f"{task.id}. 🔴 **{task.title}**\n   {priority} · Due {due}")

        await interaction.followup.send("\n".join(lines))

    @app_commands.command(
        name="today",
        description="Show tasks due today",
    )
    async def today(self, interaction: discord.Interaction):
        now = datetime.now()
        start = datetime.combine(now.date(), time.min)
        end = start + timedelta(days=1)

        async with SessionLocal() as session:
            tasks = await get_tasks_due_today(
                session,
                start,
                end,
            )

        if not tasks:
            await interaction.response.send_message("🎉 You have no tasks due today!")
            return

        lines = ["📅 **Tasks Due Today**", ""]

        for task in tasks:
            priority = task.priority.capitalize()
            due = task.due_at.strftime("%I:%M %p")

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
        priority="The new task priority",
        due="The new due date: YYYY-MM-DD HH:MM",
    )
    @app_commands.choices(
        priority=[
            app_commands.Choice(name="Low", value="low"),
            app_commands.Choice(name="Normal", value="normal"),
            app_commands.Choice(name="High", value="high"),
        ]
    )
    async def edit(
        self,
        interaction: discord.Interaction,
        task_id: int,
        title: str,
        priority: app_commands.Choice[str] | None = None,
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
            task = await edit_task(
                session,
                task_id,
                title,
                priority.value if priority else None,
                due_at,
            )

            if task is None:
                await interaction.response.send_message(
                    f"❌ Task #{task_id} was not found."
                )
                return

            await interaction.response.send_message(
                f"✏️ Updated task #{task.id}: **{task.title}**"
            )

    @app_commands.command(
        name="clear",
        description="Delete all completed tasks",
    )
    async def clear(self, interaction: discord.Interaction):
        print("CLEAR COMMAND RECEIVED", interaction.id)

        await interaction.response.defer()

        async with SessionLocal() as session:
            count = await clear_completed_tasks(session)

        if count == 0:
            await interaction.followup.send("🧹 You have no completed tasks to clear.")
            return

        await interaction.followup.send(f"🧹 Cleared **{count}** completed task(s).")


task_group = TaskGroup()
