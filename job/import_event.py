from .celery import celery_app
from core.module import event


@celery_app.task()
def write_event_for_app(data):
    # with open('/Users/datle/code/dp-api/core/module/sample_1.json') as f:
    #     data = json.load(f)
    return event.write_event_for_app(data)

@celery_app.task()
def write_event_for_web(data):
    # with open('/Users/datle/code/dp-api/core/module/sample_1.json') as f:
    #     data = json.load(f)
    return event.write_event_for_web(data)

@celery_app.task()
def write_event_for_test(data):
    return event.write_event_for_te(data)