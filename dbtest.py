import fitfile
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminDb, Attributes, ActivitiesDb, GarminSummaryDb, Activities, StepsActivities, ActivityLaps, ActivityRecords
from idbutils.list_and_dict import list_not_none

gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()


garmin_db = GarminDb(db_params_dict)
garmin_act_db = ActivitiesDb(db_params_dict)
garmin_sum_db = GarminSummaryDb(db_params_dict)
measurement_system = Attributes.measurements_type(garmin_db)
unit_strings = fitfile.units.unit_strings[measurement_system]
distance_units = unit_strings[fitfile.units.UnitTypes.distance_long]

def __report_sport(sport_col, sport):
    records = Activities.row_count(garmin_act_db, sport_col, sport)
    if records > 0:
        sport_title = sport.title().replace('_', ' ')
        total_distance = Activities.get_col_sum_for_value(garmin_act_db, Activities.distance, sport_col, sport)
        if total_distance is None:
            total_distance = 0
            average_distance = 0
        else:
            average_distance = total_distance / records
        return [sport_title, records, total_distance, average_distance]



years = Activities.get_years(garmin_act_db)
years.sort()
sports = list_not_none(Activities.get_col_distinct(garmin_act_db, Activities.sport))
sub_sports = list_not_none(Activities.get_col_distinct(garmin_act_db, Activities.sub_sport))

sports_stats = []
for sport_name in [sport.name for sport in fitfile.Sport]:
    sport_stat = __report_sport(Activities.sport, sport_name)
    if sport_stat:
        sports_stats.append(sport_stat)

def __format_activity(activity):
    if activity:
        if activity.is_steps_activity():
            steps_activity = StepsActivities.get(garmin_act_db, activity.activity_id)
            return [activity.activity_id, activity.name, activity.type, activity.sport, activity.distance, activity.elapsed_time, activity.avg_speed,
                    steps_activity.avg_pace, activity.calories, activity.training_load, activity.self_eval_feel, activity.self_eval_effort]
        return [activity.activity_id, activity.name, activity.type, activity.sport, activity.distance, activity.elapsed_time, activity.avg_speed, '',
                activity.calories, activity.training_load, activity.self_eval_feel, activity.self_eval_effort]
    return ['', '', '', '', '', '', '', '', '']

activities = Activities.get_latest(garmin_act_db, 10)
rows = [__format_activity(activity) for activity in activities]

rows = []
for display_activity in gc_config.display_activities():
    name = display_activity.activity_name().capitalize()
    rows.append([f'Latest {name}'] + __format_activity(Activities.get_latest_by_sport(garmin_act_db, display_activity)))
    rows.append([f'Fastest {name}'] + __format_activity(Activities.get_fastest_by_sport(garmin_act_db, display_activity)))
    rows.append([f'Slowest {name}'] + __format_activity(Activities.get_slowest_by_sport(garmin_act_db, display_activity)))
    rows.append([f'Longest {name}'] + __format_activity(Activities.get_longest_by_sport(garmin_act_db, display_activity)))


courses = Activities.get_col_distinct(garmin_act_db, Activities.course_id)