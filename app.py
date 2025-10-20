#!/usr/bin/env python3
"""
Habit Tracker CLI

This script provides a modern command-line interface for tracking daily habits. It uses Typer
and Rich to offer subcommands, colored output, and a neat table display.

Usage:
  python app.py --help
"""

import json
import os
from datetime import date
import typer
from rich.table import Table
from rich.console import Console

# Path to the JSON file where habits are stored
DATA_FILE = "data/habits.json"

app = typer.Typer(help="Track your daily habits with a beautiful CLI.")
console = Console()


def load_data() -> dict:
    """Load habit data from the JSON file. Returns an empty dict if the file doesn't exist."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data: dict) -> None:
    """Save habit data back to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.command()
def add(name: str = typer.Argument(..., help="Name of the new habit")) -> None:
    """Add a new habit to the tracker."""
    data = load_data()
    if name in data:
        console.print(f"[yellow]Habit '{name}' already exists.[/]")
        raise typer.Exit()
    data[name] = {"streak": 0, "last_completed": None}
    save_data(data)
    console.print(f"[green]Added habit '{name}'.[/]")


@app.command(name="list")
def list_habits() -> None:
    """List all habits with their current streak and last completion date."""
    data = load_data()
    if not data:
        console.print("[cyan]No habits found. Add one with `python app.py add`.")
        return
    table = Table(title="Your Habits", box=None, show_header=True, header_style="bold magenta")
    table.add_column("Habit", style="cyan", no_wrap=True)
    table.add_column("Streak", justify="right", style="green")
    table.add_column("Last Completed", style="yellow")
    for name, info in data.items():
        last = info["last_completed"] or "-"
        table.add_row(name, str(info["streak"]), last)
    console.print(table)


@app.command()
def complete(name: str = typer.Argument(..., help="Name of the habit to mark as completed")) -> None:
    """Mark a habit as completed for today and update its streak."""
    data = load_data()
    if name not in data:
        console.print(f"[red]Habit '{name}' not found.[/]")
        raise typer.Exit(code=1)
    today = date.today().isoformat()
    info = data[name]
    if info["last_completed"] == today:
        console.print(f"[yellow]Habit '{name}' is already marked as completed today.[/]")
        return
    # Update streak depending on whether yesterday was the last completion date
    if info["last_completed"]:
        last_date = date.fromisoformat(info["last_completed"])
        if (date.today() - last_date).days == 1:
            info["streak"] += 1
        else:
            info["streak"] = 1
    else:
        info["streak"] = 1
    info["last_completed"] = today
    save_data(data)
    console.print(f"[bold green]Completed '{name}'! New streak: {info['streak']}[/]")


@app.command()
def delete(name: str = typer.Argument(..., help="Name of the habit to delete")) -> None:
    """Delete a habit from the tracker."""
    data = load_data()
    if name not in data:
        console.print(f"[red]Habit '{name}' not found.[/]")
        raise typer.Exit(code=1)
    data.pop(name)
    save_data(data)
    console.print(f"[green]Deleted habit '{name}'.[/]")


if __name__ == "__main__":
    app()
