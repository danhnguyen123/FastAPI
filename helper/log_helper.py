from config import config
# from mixpanel import Mixpanel
from datetime import datetime
import functools
import time

# mp = Mixpanel('da1db92030901bdb78431cd88d16d273')

def build_detail(status,detail,action,name):
    detail['status'] = status
    detail['action'] = action
    detail['env'] = config.ENV
    detail['event_name'] = name
    name  = '[{}] {}'.format(config.ENV,name)
    event_name = status + ": " + action

    if config.ENV == 'localhost':
        print('-'*50)
        print(datetime.now(),status, action, detail)

    return detail, name, event_name


def info(action, detail = {}, name = "Undefine"):
    detail, name, event_name = build_detail("INFO",detail,action,name)
    # mp.track(distinct_id = name ,event_name = event_name ,properties = detail)

def warning(action, detail = {}, name = "Undefine"):
    detail, name, event_name = build_detail("WARRNING",detail,action,name)
    # mp.track(distinct_id = name ,event_name = event_name ,properties = detail)

def error(action, detail = {}, name = "Undefine"):
    detail, name, event_name = build_detail("ERROR",detail,action,name)
    # mp.track(distinct_id = name ,event_name = event_name ,properties = detail)


# This decorator can be applied to any job function to log the elapsed time of each job @print_elapsed_time
def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed in %d seconds' % (func.__name__, time.time() - start_timestamp))
        return result

    return wrapper
