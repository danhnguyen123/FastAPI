from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
from config import config
import pytz

def get_now():
    return datetime.now(pytz.utc)

def get_today():
    return date.today()

def get_start_date_of_month(date = date.today()):
    return date.replace(day=1)

def get_end_date_of_month(date = date.today()):
    first_date_next_month = date + relativedelta(months=+1)
    # print(date,first_date_next_month)
    return first_date_next_month.replace(day=1) - timedelta(days=1)

def get_interval_time(is_plus = False,day_count = 0, hour_count = 0, minute_count = 0, month_count = 0):
    if is_plus:
        return get_now() + relativedelta(months=+month_count ,days=+day_count, hours=+hour_count, minutes=+minute_count)
    return get_now()- relativedelta(months=+month_count, days=+day_count, hours=+hour_count, minutes=+minute_count)

def get_interval_time_from(time,is_plus = False,day_count = 0, hour_count = 0, minute_count = 0, month_count = 0):
    if is_plus:
        return time + relativedelta(months=+month_count ,days=+day_count, hours=+hour_count, minutes=+minute_count)
    return time - relativedelta(months=+month_count, days=+day_count, hours=+hour_count, minutes=+minute_count)

def get_interval_day(day,is_plus = False,day_count = 0,month_count = 0):
    if is_plus:
        return day + relativedelta(days=+day_count,months=+month_count)
    return day - relativedelta(days=+day_count,months=+month_count)

def convert_to_sql_format(input_datetime):
    return input_datetime.strftime("%Y-%m-%d %H:%M:%S")

def format_api_finan(input_datetime):
    try:
        return input_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    except:
        return datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def updated_at():
    return get_now().strftime("%Y-%m-%d %H:%M:%S")

def time_obj_from_string(string):
    time_object = datetime.strptime(string,"%Y-%m-%d %H:%M:%S")
    return time_object

def timestamp_to_datetime(timestamp):
    time_object = datetime.fromtimestamp(timestamp)
    return time_object.strftime("%Y-%m-%d %H:%M:%S")

def datetime_to_timestamp(_datetime):
    time_object = datetime.timestamp(_datetime)
    return int(time_object)

def shopee_time_from_string(string):
    return datetime_to_timestamp(time_obj_from_string(string))

def convert_utc_to_local(input_datetime, sql_format = True):
    if sql_format:
        return input_datetime.tz_convert(config.DWH_TIMEZONE).strftime(config.DWH_TIME_FORMAT)
    else:
        return input_datetime.tz_convert(config.DWH_TIMEZONE)

def is_out_of_working_support_hour(from_hour = 7,to_hour = 22):
    tz = pytz.timezone(config.DWH_TIMEZONE)
    if (datetime.now(tz).hour > from_hour) and (datetime.now(tz).hour < to_hour):
        return False
    else:
        print("off time")
        return True
