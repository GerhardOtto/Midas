import argparse
import icalendar
from datetime import datetime, timedelta
import os

def check_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower() == '.ics'

def read_ics_file(file_path):
    if not check_file_extension(file_path):
        print(f"Error: '{file_path}' is not a valid .ics file.")
        return {}

    events_by_month = {}

    with open(file_path, 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())
        for event in cal.walk('vevent'):
            start_time = event.get('dtstart').dt
            month_key = (start_time.year, start_time.month)

            if month_key not in events_by_month:
                events_by_month[month_key] = {}

            summary = event.get('summary')
            if summary not in events_by_month[month_key]:
                events_by_month[month_key][summary] = []

            events_by_month[month_key][summary].append({
                'start_time': start_time,
                'end_time': event.get('dtend').dt,
            })

    return events_by_month

def calculate_duration(events):
    total_duration = timedelta()

    for event in events:
        total_duration += event['end_time'] - event['start_time']

    return total_duration

def calculate_salary(total_duration, hourly_wage):
    total_hours = total_duration.total_seconds() / 3600
    return total_hours * hourly_wage

def print_events_by_month(events_by_month, hourly_wage):
    for month, summaries in sorted(events_by_month.items()):
        month_name = datetime(month[0], month[1], 1).strftime("%B %Y")
        print(f'{month_name}:')
        total_duration_month = timedelta()
        for summary, events in summaries.items():
            total_duration = calculate_duration(events)
            total_duration_month += total_duration
            total_hours = total_duration.total_seconds() / 3600
            print(f'  Summary: {summary}')
            print(f'    Total Duration: {total_hours:.2f} hours')
            print()
        total_hours_month = total_duration_month.total_seconds() / 3600
        print(f'  Total Duration: {total_hours_month:.2f} hours')
        monthly_salary = calculate_salary(total_duration_month, hourly_wage)
        print(f'  Monthly Salary: R{monthly_salary:.2f}')
        print()

if __name__ == '__main__':
    hourly_wage = float(input("Enter your hourly wage in USD: "))
    file_path = input("Enter the path to the ICS file (e.g., calendar.ics): ")

    if not check_file_extension(file_path):
        exit()

    events_by_month = read_ics_file(file_path)
    print_events_by_month(events_by_month, hourly_wage)
