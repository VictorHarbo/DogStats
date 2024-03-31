import logging
import json
import fitfile
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

def latest_activities(amount):
    activities = Activities.get_latest(garmin_act_db, 10)
    json_activities = json.dumps(activities)
    return json_activities


# Correct way of accessing variables inside objects
def stepsForDate(date):    
    content = DaysSummary.get_day(garmin_sum_db, date)
    logger.warning(content)
    return str(getattr(content, "steps"))

def all_steps():
    """Create a dict with dates as keys and the amount of steps walked that day as values."""
    allRecords =  DaysSummary.get_all(garmin_sum_db)
    allSteps = {}

    for record in allRecords:
        date = str(getattr(record, "day"))
        steps = getattr(record, "steps")
        allSteps[date] = steps

    return allSteps


