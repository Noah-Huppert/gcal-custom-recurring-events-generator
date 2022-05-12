# GCal Custom Recurring Events Generator
Generates an `.ics` calendar file with a custom reoccurring event type.

# Table Of Contents
- [Overview](#overview)
- [Usage](#usage)

# Overview
A utility with the ability to generate a `.ics` calendar file which contains reoccurring events which match both criteria

- Occur on a certain day
- Occur only if the date is even or odd

# Usage
[Pipenv](https://pipenv.pypa.io) is required.

1. Install dependencies:
   ```bash
   pipenv install
   ```
2. Activate the virtual environment:
   ```bash
   pipenv shell
   ```
   Run all following commands in this shell.
3. Run the script:
   ```bash
   ./generate.py \
     --out-ics trash.ics \
	 --start-date 2022-1-1 \
	 --end-date 2023-1-1 \
	 --occurs-on-day tuesday \
	 --occurs-odd-or-even even \
	 --event-time-start "7:30 pm" \
	 --event-time-end "7:45 pm" \
	 --event-attendee "email@email.com" \
	 --event-attendee "another@email.com" \
	 --event-name "Take Out Trash"
   ```


