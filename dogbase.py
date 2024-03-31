import logging
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminDb, Attributes, File, ActivitiesDb, GarminSummaryDb, Activities, DaysSummary, StepsActivities

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Garmin DB setup
gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
garmin_db = GarminDb(db_params_dict)
garmin_act_db = ActivitiesDb(db_params_dict)
garmin_sum_db = GarminSummaryDb(db_params_dict)



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


