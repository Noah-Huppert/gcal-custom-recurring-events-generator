#!/usr/bin/env python3
from ics import Calendar, Event

import argparse
from datetime import date, datetime, timedelta, timezone, tzinfo

class DateRangeIter:
    start: date
    end: date
    
    current: date

    def __init__(self, start: date, end: date):
        self.current = start
        self.start = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        to_return = self.current
        if to_return > self.end:
            raise StopIteration
        
        self.current += timedelta(days=1)
        return to_return

WEEKDAY_STR_TO_INT = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
}

def main():
    # Arguments
    parser = argparse.ArgumentParser(description="Generates a set of .ics files for trash takeout events")
    parser.add_argument("--out-ics",
                        help="The file where the calendar .ics file will be written",
                        required=True,
                        default="trash.ics")
    parser.add_argument("--start-date",
                        help="The date on which events will start (format: Y-m-d)",
                        required=True,
                        type=lambda s: datetime.strptime(s, '%Y-%m-%d').date())
    parser.add_argument("--end-date",
                        help="The date on which events will start (format: Y-m-d)",
                        required=True,
                        type=lambda s: datetime.strptime(s, '%Y-%m-%d').date())
    parser.add_argument("--occurs-on-day",
                        help="Indicates which day of the week the event should occur",
                        choices=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
                        required=True)
    parser.add_argument("--occurs-odd-or-even",
                        help="Indicates if the event occurs on an odd or even date, criteria is combined with --occurs-on-day",
                        choices=["odd", "even"],
                        required=True)
    parser.add_argument("--event-name",
                        help="The name of the event",
                        required=True)
    parser.add_argument("--event-time-start",
                        help="The time at which the event will occur (format: H:M AM/PM)",
                        type=lambda s: datetime.strptime(s, '%I:%M %p'),
                        required=True)
    parser.add_argument("--event-time-end",
                        help="The time at which the event will stop occuring (format: H:M AM/PM)",
                        type=lambda s: datetime.strptime(s, '%I:%M %p'),
                        required=True)
    parser.add_argument("--event-attendee",
                        help="Email of an attendee",
                        action='append',
                        required=False,
                        default=[])
    
    args = parser.parse_args()

    user_tz = datetime.now(timezone.utc).astimezone().tzinfo

    # Iterate through days
    calendar = Calendar()
    num_events = 0
    for current_date in DateRangeIter(args.start_date, args.end_date):
        # If matches the criteria
        if current_date.weekday() == WEEKDAY_STR_TO_INT[args.occurs_on_day] and current_date.day % 2 == (0 if args.occurs_odd_or_even == "even" else 1):
            # Craft event
            num_events += 1
            
            event = Event()
            event.name = args.event_name

            event.begin = datetime(
                day=current_date.day,
                month=current_date.month,
                year=current_date.year,
                hour=args.event_time_start.hour,
                minute=args.event_time_start.minute,
                tzinfo=user_tz,
            ).astimezone(timezone.utc)
            event.end = datetime(
                day=current_date.day,
                month=current_date.month,
                year=current_date.year,
                hour=args.event_time_end.hour,
                minute=args.event_time_end.minute,
                tzinfo=user_tz,
            ).astimezone(timezone.utc)
            for attendee_email in args.event_attendee:
                event.add_attendee(f"mailto:{attendee_email}")

            # Add to calendar
            calendar.events.add(event)

    # Write to file
    with open(args.out_ics, 'w') as ics_f:
        ics_f.writelines(calendar)

    print(f"Wrote {num_events} event(s) to {args.out_ics}")

if __name__ == "__main__":
    main()
