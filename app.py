"""Simple command-line habit tracking app.

This module provides a CLI for creating and completing daily habits.
Data is persisted to a JSON file in the project directory.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path("data") / "habits.json"


@dataclass
class Habit:
    """Represent a tracked habit."""

    name: str
    streak: int = 0
    last_completed: str | None = None

    def mark_complete(self, today: date) -> None:
        """Update the habit's streak when completed for ``today``.

        If the habit was completed yesterday, the streak increments.
        Otherwise the streak resets to 1 for today.
        """

        today_str = today.isoformat()
        if self.last_completed == (today - date.resolution).isoformat():
            self.streak += 1
        else:
            self.streak = 1
        self.last_completed = today_str


class HabitStore:
    """Manage loading and saving habits from disk."""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Habit]:
        if not self.storage_path.exists():
            return {}
        with self.storage_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return {name: Habit(**info) for name, info in data.items()}

    def save(self, habits: Dict[str, Habit]) -> None:
        with self.storage_path.open("w", encoding="utf-8") as fh:
            json.dump({name: asdict(habit) for name, habit in habits.items()}, fh, indent=2)


class HabitApp:
    """CLI interface for managing habits."""

    def __init__(self, store: HabitStore) -> None:
        self.store = store

    def add_habit(self, name: str) -> str:
        habits = self.store.load()
        if name in habits:
            return f"Habit '{name}' already exists."
        habits[name] = Habit(name=name)
        self.store.save(habits)
        return f"Added habit '{name}'."

    def list_habits(self) -> List[str]:
        habits = self.store.load()
        if not habits:
            return ["No habits tracked yet. Use 'add' to create one."]
        lines = ["Your habits:"]
        for habit in habits.values():
            last_completed = habit.last_completed or "Never"
            lines.append(f"- {habit.name} (streak: {habit.streak}, last completed: {last_completed})")
        return lines

    def complete_habit(self, name: str) -> str:
        habits = self.store.load()
        if name not in habits:
            return f"Habit '{name}' is not being tracked."
        habit = habits[name]
        habit.mark_complete(date.today())
        habits[name] = habit
        self.store.save(habits)
        return f"Nice! '{name}' streak is now {habit.streak}."

    def delete_habit(self, name: str) -> str:
        habits = self.store.load()
        if habits.pop(name, None) is None:
            return f"Habit '{name}' was not found."
        self.store.save(habits)
        return f"Removed habit '{name}'."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track daily habits and maintain streaks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name", help="Name of the habit to track")

    complete_parser = subparsers.add_parser("complete", help="Mark a habit as done today")
    complete_parser.add_argument("name", help="Name of the habit to mark complete")

    delete_parser = subparsers.add_parser("delete", help="Stop tracking a habit")
    delete_parser.add_argument("name", help="Name of the habit to delete")

    subparsers.add_parser("list", help="List all habits and streaks")
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = HabitApp(HabitStore(DATA_FILE))

    if args.command == "add":
        message = app.add_habit(args.name)
        print(message)
    elif args.command == "complete":
        message = app.complete_habit(args.name)
        print(message)
    elif args.command == "delete":
        message = app.delete_habit(args.name)
        print(message)
    elif args.command == "list":
        for line in app.list_habits():
            print(line)


if __name__ == "__main__":
    main()
