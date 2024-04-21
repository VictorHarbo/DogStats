import logging
import configparser
from datetime import datetime
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminDb, Attributes, File, ActivitiesDb, GarminSummaryDb, Activities, DaysSummary, StepsActivities

# Config and log setup
config = configparser.ConfigParser()
config.read("config.ini")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Garmin DB setup
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)
garmin_act_db = ActivitiesDb(db_params_dict)
garmin_sum_db = GarminSummaryDb(db_params_dict)

# Date of dog in life 
DOG_DATE = config["config"].get("dog_date")




def overview():
    """
    Get an overview of the backing GarminDB instance.
    Shows information on amount of records in different parts of the DB and variables in each part.
    """
    #measurement_system = Attributes.measurements_type(garmin_db)
    #unit_strings = fitfile.units.unit_strings[measurement_system]
    #distance_units = unit_strings[fitfile.units.UnitTypes.distance_long]

    file_stats = [
        ['All', File.row_count(garmin_db)]
    ]
    for file_type_name in [file_type.name for file_type in File.FileType]:
        records = File.row_count(garmin_db, File.type, file_type_name)
        if records > 0:
            file_stats.append([file_type_name, records])

    file_stats.append(["ActivitiesDB", Activities.col_names])
    file_stats.append(["SummaryDB", DaysSummary.col_names])
    

    return file_stats

# Correct way of accessing variables inside objects
def steps_for_date(date):    
    """
    Get amount of steps for a given date.
    
    Params:
     date (string): A date string in the format: YYYY-MM-DD
    """
    single_day = DaysSummary.get_day(garmin_sum_db, date)
    # Logging to figure what is inside a DaysSymmary class.
    logger.warning(single_day)
    return str(getattr(single_day, "steps"))

def all_steps():
    """Create a dict with dates as keys and the amount of steps walked that day as values."""
    allRecords =  DaysSummary.get_all(garmin_sum_db)
    all_steps = {}

    for record in allRecords:
        date = str(getattr(record, "day"))
        steps = getattr(record, "steps")
        all_steps[date] = steps

    return all_steps

def steps_before_dog():
    """
    Get a dict of dates with amount of steps as values for all dates until a dog came into your application.
    """
    # Create a datetime object for a specific date
    start_date = datetime(2000, 1, 1).date()

    records_before_dog = DaysSummary.get_for_period(garmin_sum_db, start_date, dog_date())
    steps_before_dog = {}

    for record in records_before_dog:
        date = str(getattr(record, "day"))
        steps = getattr(record, "steps")
        steps_before_dog[date] = steps

    return steps_before_dog
    

def steps_since_dog():
    """
    Get a dict of dates with amount of steps as values for all dates since a dog came into your application.
    """

    # Get the current date
    today_date = datetime.now().date()

    records_after_dog = DaysSummary.get_for_period(garmin_sum_db, dog_date(), today_date)
    steps_after_dog = {}

    for record in records_after_dog:
        date = str(getattr(record, "day"))
        steps = getattr(record, "steps")
        steps_after_dog[str(date)] = int(steps)

    return steps_after_dog

def dog_date():
    """Parse the date of acquireing a dog from config as a date object, Expects a string in the format YYYY-MM-DD."""
    return datetime.strptime(DOG_DATE, "%Y-%m-%d").date()

def get_activities():
    """get all activities in the DB
    """
    allRecords =  Activities.get_all(garmin_act_db)
    return allRecords


def get_activies_of_type(type):
    """Get all activities of a given type from the DB
    Args:
        type (String): Type of activities to fetch from DB.
    """
    activities = Activities.get_by_sport(garmin_act_db, type)
    return activities

def get_activities_with_name(name):
    """_summary_

    Args:
        name (_type_): _description_
    """
    all_activities = Activities.get_all(garmin_act_db)
    
    activities_with_name = []
    
    for entry in all_activities:
        if entry.name == name:
            activities_with_name.append(entry)
    
    return activities_with_name