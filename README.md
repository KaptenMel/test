# Habit Tracker CLI

A simple command-line app for keeping track of daily habits and maintaining completion streaks.

## Features

- Add new habits to track.
- List all habits with their current streak and last completion date.
- Mark a habit as complete for today to extend its streak.
- Delete habits you no longer want to track.

Habits are stored in `data/habits.json`, which is created automatically the first time you run the app.

## Requirements

- Python 3.10 or later (uses modern typing features).

## Usage

```bash
python app.py add "Meditate"
python app.py list
python app.py complete "Meditate"
python app.py delete "Meditate"
```

Use `python app.py --help` to see the full list of commands and options.
