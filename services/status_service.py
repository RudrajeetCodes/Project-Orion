from services.task_service import get_task_stats
from services.reminder_service import get_reminders


async def build_status(session) -> str:
    task_stats = await get_task_stats(session)
    reminders = await get_reminders(session)

    active_reminders = sum(not reminder.sent for reminder in reminders)

    return (
        "```text\n"
        "ORION v0.1.0\n"
        "────────────────────────────\n"
        "$ system.status()\n"
        "\n"
        "[ TASKS ]\n"
        f"  total      {task_stats['total']}\n"
        f"  completed  {task_stats['completed']}\n"
        f"  pending    {task_stats['incomplete']}\n"
        "\n"
        "[ REMINDERS ]\n"
        f"  total      {len(reminders)}\n"
        f"  active     {active_reminders}\n"
        "\n"
        "[ SYSTEM ]\n"
        "  database   ONLINE\n"
        "  scheduler  ONLINE\n"
        "────────────────────────────\n"
        "> system operational\n"
        "```"
    )