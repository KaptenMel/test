# Habit Tracker

Habit Tracker is a polished command‑line tool for creating and maintaining daily habits. It's built with Python using [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/) to provide an ergonomic interface, colorized output and tables.

## Features

- Add new habits to track and store them persistently.
- View your current habits in a colorful table with streak and last completion.
- Mark a habit as completed for today; streaks automatically update and reset if you miss a day.
- Delete habits you no longer track.
- Modern command‑line interface with helpful commands (`--help`) and pretty output.

## Requirements

- Python 3.10 or later
- [`typer`](https://pypi.org/project/typer/) (install with `pip install typer[all]`)
- [`rich`](https://pypi.org/project/rich/)

## Installation

Install the dependencies with pip:

```bash
pip install typer[all] rich
```

## Usage

Add a habit:

```bash
python app.py add "meditate"
```

List all habits:

```bash
python app.py list
```

Complete a habit:

```bash
python app.py complete "meditate"
```

Delete a habit:

```bash
python app.py delete "meditate"
```

To see all available commands, run:

```bash
python app.py --help
```

## Data Storage

Habit data is stored as JSON in `data/habits.json`. The file is created automatically the first time you add a habit.

Feel free to customize the code or styling in `app.py`.
