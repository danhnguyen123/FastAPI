from core.database import SessionLocal
from core.model import event
from urllib.parse import urlparse
from config import config
from datetime import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy import text
import pandas as pd
import json 
from helper import db_helper

# mp = Mixpanel(config.MIXPANEL_API_KEY)
# api_key = config.MIXPANEL_API_KEY
# api_secret = config.MIXPANEL_API_SECRET

def write_event_for_app(data):
    if data['type'] not in ('track','page'): ## Only accept type : track, page
        return "SKIP"
    if 'event' not in data: ## Only accept type : track, page
        return "SKIP"

    ## transformation
    transforma_data = {
        'user_id' : data.get('user_id'),
        'event_at' : data['event_at'],
        'event_name' : data['event_name'],
        'title' : data['title'],
        'content' : data['content'],
        'data' : data['data'],
        'message_id' : data['message_id'],
        'app_version' : data['app_version'],
        'app_build' : data['app_build'],
        'anonymous_id' : data['anonymous_id'],
    }
    ## transformation

    insert_to_db = event.EventAppModel(**transforma_data)

    db = SessionLocal()
    try:
        db.add(insert_to_db)
        db.commit()
    except:
        db.rollback()
        return False
    db.close()

    return True

def write_event_for_web(data):
    ## Only accept type : page
    if data['type'] not in ('page'):
        return "SKIP"

    row = {}
    row['anonymous_id'] = data['anonymous_id']
    row['message_id'] = data['message_id']
    row['user_id'] = data['user_id']
    row['event_at'] = data['timestamp']
    row['path'] = data['path']
    row['referrer'] = data['referrer']
    row['search'] = data['search']
    row['title'] = data['title']
    row['url'] = data['url']
    row['domain'] = urlparse(data['properties']['url']).netloc

    insert_to_db = event.EventWebModel(**row)

    db = SessionLocal()
    try:
        db.add(insert_to_db)
        db.commit()
    except:
        db.rollback()
        return False
    db.close()
    return True

# def sync_web_event_to_postgress():
#     bq_engine = create_engine('bigquery://'+config.BIGQUERY_PROJECT_ID)
#     execute_query = """
#         SELECT distinct any_value(user_id) user_id,any_value(user_pseudo_id) as anonymous_id
#             ,max(datetime(timestamp_micros(event_timestamp),'Asia/Ho_Chi_Minh')) event_at
#             ,any_value(device.web_info.hostname) as domain
#             ,user_pseudo_id || '.' || event_timestamp as message_id
#         FROM `finan-1ae3f.analytics_276366457.events_intraday_*`
#         where event_timestamp > UNIX_MICROS(TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 MINUTE))
#         GROUP BY message_id
#     """
#     df = pd.read_sql(text(execute_query),con=bq_engine)
#     pg_connection = {'driver':'psycopg2','engine' : create_engine(config.get_BI_DB_URL())}
#     db_helper.upsert(connection=pg_connection, update_data=df, table_name='event_web_realtime', db_schema='finan', pk_array=['message_id'])
#     return True


def write_event_for_te(data):
    row = {
    'user_id' : data['user_id'],
    'event_name' : data['event_name'],
    'message_id' : data['message_id']
    }
    insert_to_db = event.EventTestModel(**row)

    db = SessionLocal()
    try:
        db.add(insert_to_db)
        db.commit()
    except:
        db.rollback()
        return False
    db.close()
    return True