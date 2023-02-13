from fastapi import APIRouter, Depends, HTTPException, Request

from api.dependencies import get_token_header
from job.celery import celery_app
from pydantic import BaseModel, Field
import json 

# from job.import_event import write_event_for_test

router = APIRouter(
    prefix="/webhook",
    tags=["public-webhook"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/segment/web", dependencies=[Depends(get_token_header)])
async def segment_web_hook(request: Request):
    data = await request.json()
    task_id = celery_app.send_task("job.import_event.write_event_for_web", args=[data])
    return {'task_id' : str(task_id)}

@router.post("/segment/app", dependencies=[Depends(get_token_header)])
async def segment_web_hook(request: Request):
    data = await request.json()
    task_id = celery_app.send_task("job.import_event.write_event_for_app", args=[data])
    return {'task_id' : str(task_id)}


class Item(BaseModel):
    user_id : str = Field("7f856768-ab3b-11ed-afa1-0242ac120002", title='User ID', description='User ID description')
    event_name : str = Field("screen_name", title='Event name', description='Event name description')
    message_id : str = Field("6bbedb9a-ab3d-11ed-afa1-0242ac120002", title='Message ID', description='Message ID description')

@router.post("/segment/test", dependencies=[Depends(get_token_header)])
async def segment_test(request: Item):
    
    request = request.__dict__
    data = request
    # write_event_for_test(data)
    task_id = celery_app.send_task("job.import_event.write_event_for_test", args=[data], queue='default')
    return data
    # return True