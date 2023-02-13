from .celery import celery_app
from core.module import event


# @celery_app.task()
# def write_event_for_app(data):
#     # with open('/Users/datle/code/dp-api/core/module/sample_1.json') as f:
#     #     data = json.load(f)
#     return event.write_event_for_app(data)

# @celery_app.task()
# def write_event_for_web(data):
#     # with open('/Users/datle/code/dp-api/core/module/sample_1.json') as f:
#     #     data = json.load(f)
#     return event.write_event_for_web(data)

# @celery_app.task()
# def sync_web_event_to_postgress():
#     return event.sync_web_event_to_postgress()


@celery_app.task()
def test(data):
    print("Print Hello World")
    return "Return Hello World"

@celery_app.task()
def test_data():
    data = {
        "user_id": "8c53efb2-aaac-11ed-afa1-0242ac120002",
        "event_name": "test",
        "message_id": "ahihi123"
        }

    event.write_event_for_test(data)
    print("Print Hello World")
    return "Return Hello World"