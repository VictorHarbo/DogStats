import pandas as pd
import datetime

from dogbase import steps_since_dog, get_activies_of_type, get_activities_with_name
from collections import deque

def seven_days_of_steps():
    """ Get the last seven days of steps data from GarminDB.

    Returns:
        Dict: A dictionary with keys being dates and values being steps for the day.
    """
    # Method to extract steps from GarminDB
    steps = steps_since_dog()

    dict_deque = deque(steps.items())

    last_seven_entries = []
    for _ in range(min(len(dict_deque), 7)):
        last_seven_entries.append(dict_deque.pop())
        
    last_seven_entries = last_seven_entries[::-1]

    last_seven_dict = dict(last_seven_entries)
    formatted_dict = {str(key): int(value) for key, value in last_seven_dict.items()}
    return formatted_dict


def runs_per_week():
    """ Get a Pandas dataframe containing the amount of runs pr week since the start of 2024

    Returns:
        Dataframe: Dataframe with a single column containing amount of runs pr week since 2024
    """
    activities = get_activies_of_type("running")

    #print(activities)

    datetimes = []

    for activity in activities:
        datetimes.append(activity.start_time)

    datetimes = pd.to_datetime(datetimes)

    df = pd.DataFrame({'datetime': datetimes})

    # Filter datetimes before 2024
    df = df[df['datetime'].dt.year >= 2024]

    weekly_counts = df.groupby([df['datetime'].dt.year, df['datetime'].dt.isocalendar().week]).size()
    weekly_counts = weekly_counts.reset_index()
    
    weekly_counts = weekly_counts.rename(columns={0: "count"})
    
    return weekly_counts

def plank_minuts_pr_week():
    """Get a dictionary of plank duration per day

    Returns:
        Dict(Datetime, Datetime)}: A dictionary containing a start time for planks as keys and contains the duration of the planks as values.
    """
    
    planks = get_activities_with_name("Plank")

    simple_planks = {}
    
    for plank in planks:
        simple_planks[plank.start_time] = plank.moving_time
        
        
    # Group durations by week
    durations_per_week = {key: datetime.timedelta() for key in range(1, 53)}

    for date, duration in simple_planks.items():
        # Calculate ISO week number
        week_number = date.isocalendar()[1]
        # Add duration to the corresponding week
        if week_number not in durations_per_week:
            durations_per_week[week_number] = datetime.timedelta()  # Initialize duration to zero
        durations_per_week[week_number] += datetime.timedelta(hours=duration.hour, minutes=duration.minute)

    return durations_per_week
    