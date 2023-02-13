from dotenv import load_dotenv
load_dotenv()

from config import config
from celery import Celery

BROKER_URI = config.CELERY_BROKER_URL
BACKEND_URI = config.CELERY_RESULT_BACKEND

celery_app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=[
        'job.test',
        'job.import_event',
        # 'job.ecom',
        # 'job.notification',
        # 'job.alert'
    ]
)

celery_app.conf.timezone = 'Asia/Ho_Chi_Minh'

from celery.schedules import crontab
# celery_app.conf.beat_schedule = {
#     'update_ecom_shop':{
#         'task': 'job.ecom.update_all_shop',
#         'schedule': crontab(minute='*/1'),
#         'options': {'queue' : 'all_shop'}
#     },
#     'update_web_event':{
#         'task': 'job.import_event.sync_web_event_to_postgress',
#         'schedule': crontab(minute='*/1')
#     },
#     'ecom_clean_zoombie_job':{
#         'task': 'job.ecom.clean_zoombie_job',
#         'schedule': crontab(minute='*/10'),
#         'options': {'queue' : 'all_shop'}
#     },
#     'nofitication_run':{
#         'task': 'job.notification.trigger_nofitication_run',
#         'schedule': crontab(minute='*/1')
#     },
#     'trigger_auto_message':{
#         'task': 'job.notification.trigger_auto_message',
#         'schedule': crontab(minute='*/5')
#     },
#     'timing_check':{
#         'task': 'job.alert.job_timing_check',
#         'schedule': crontab(minute='*/5')
#     }
# }

#
# from celery.signals import worker_ready
# @worker_ready.connect
# def at_start(sender, **kwargs):
#     """Run tasks at startup"""
#     with sender.app.connection() as conn:
#         sender.app.send_task("app.worker.tasks_daily_update_data.update_value_for_feature", connection=conn)
#         sender.app.send_task("app.worker.tasks.update_database_gt_duplicate", connection=conn)
#         sender.app.send_task("app.worker.tasks_update_segment.update_segment_data_from_mountaineye_db", connection=conn)

import subprocess


def start_worker():
    print("Start worker")
    subprocess.run('celery -A job.celery_app worker -l INFO -c {}'.format(config.NUMBER_OF_WORKER), shell=True)

def start_beat():
    print("Start beat")
    subprocess.run('celery -A job.celery_app beat', shell=True)
