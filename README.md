# Project Orion

Orion is a Discord bot that manages personal tasks and reminders through slash commands. It stores data in a local SQLite database and runs a background worker to deliver reminder notifications.

## Table of Contents

- Description
- Features
- Requirements
- Installation
- Configuration
- Usage
- Project Structure
- Tests
- Database Migrations

## Features

- Create, list, complete, edit, delete, and clear tasks with optional priority and due dates.
- Create, list, edit, and cancel reminders with a specific date and time.
- View overdue tasks and tasks due today.
- Display task statistics and active reminder counts.
- Maintain a dynamic status message on a configured Discord channel.
- Background worker sends pending reminder notifications to the bot owner every 10 seconds.

## Requirements

- Python 3.14 or higher
- `discord.py>=2.7.1`, `python-dotenv`, `sqlalchemy`, `aiosqlite`, `alembic`

## Installation

Clone the repository. Create a `.env` file from the provided example.

```bash
cp .env.example .env
```

Install the package in editable mode.

```bash
pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and set the following environment variables:

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Discord bot token |
| `GUILD_ID` | Discord guild ID |
| `OWNER_ID` | Discord user ID of the bot owner |
| `STATUS_CHANNEL_ID` | Discord channel ID for the status message |
| `STATUS_MESSAGE_ID` | Optional existing message ID to update; omit to create a new message |

## Usage

Start the application to initialize the database and run the bot.

```bash
python main.py
```

Once the bot is online, use slash commands in your Discord guild:

- `/task`
  - `add` — create a task with title, optional priority, and optional due date.
  - `list` — list all tasks.
  - `overdue` — list overdue tasks.
  - `today` — list tasks due today.
  - `complete` — mark a task as completed.
  - `delete` — remove a task.
  - `edit` — update a task's title, priority, or due date.
  - `clear` — delete all completed tasks.
  - `stats` — display task statistics.
- `/remind`
  - `add` — schedule a reminder with a message and date/time.
  - `list` — list all reminders.
  - `cancel` — remove a reminder by ID.
  - `edit` — update a reminder's message and date/time.
- `/ping` — check if the bot is online.

The status message on the configured channel updates after task creation or completion.

## Project Structure

```
├── alembic.ini
├── bot/              # Discord client and slash command groups
├── database/         # SQLAlchemy models, engine, and session
├── migrations/       # Alembic migration scripts
├── services/         # Business logic for tasks, reminders, and status
├── tests/            # Unit tests
├── workers/          # Background tasks
├── config.py         # Environment variable loading
├── main.py           # Application entry point
└── pyproject.toml    # Project metadata and dependencies
```

## Tests

Run the test suite with pytest.

```bash
pytest
```

## Database Migrations

Alembic manages schema changes. Apply migrations from the repository root.

```bash
alembic upgrade head
```

View migration history.

```bash
alembic history
```

The current schema includes the `tasks` and `reminders` tables, with columns for due dates, priorities, and sent status.