from services.reminder_service import get_reminders
from services.task_service import get_task_stats


async def build_status(session) -> str:
    task_stats = await get_task_stats(session)
    reminders = await get_reminders(session)

    active_reminders = sum(not reminder.sent for reminder in reminders)

    return (
        "```text\n"
        "ORION // PERSONAL COMMAND CENTER\n"
        "v0.1.0 | SYSTEM ONLINE\n"
        "\n"
        "$ status\n"
        "\n"
        "[ TASKS ]\n"
        f"  total      : {task_stats['total']}\n"
        f"  completed  : {task_stats['completed']}\n"
        f"  pending    : {task_stats['incomplete']}\n"
        "\n"
        "[ REMINDERS ]\n"
        f"  total      : {len(reminders)}\n"
        f"  active     : {active_reminders}\n"
        "\n"
        "[ SYSTEM ]\n"
        "  database   : ONLINE\n"
        "  scheduler  : ONLINE\n"
        "  discord    : ONLINE\n"
        "\n"
        "------------------------------------------\n"
        "> all systems operational\n"
        "```"
    )
