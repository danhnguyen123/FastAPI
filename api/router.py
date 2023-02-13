from fastapi import APIRouter, Depends, HTTPException, status

from .dependencies import get_token_header
from .public import webhook
# from .internal import traffic
# from .internal import tagging
# from .internal import chat

## Public
public_router = APIRouter(
    prefix="/public",
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
public_router.include_router(webhook.router)

## Internal
# internal_router = APIRouter(
#     prefix="/internal",
#     # dependencies=[Depends(get_token_header)],
#     responses={404: {"description": "Not found"}},
# )
# internal_router.include_router(traffic.router)
# internal_router.include_router(tagging.router)
# internal_router.include_router(chat.router)

## Status
router_status = APIRouter(
    prefix="/status",
    tags=["root"],
    responses={200: {"status": 200}},
)

@router_status.get("/", status_code=status.HTTP_200_OK)
async def status():
    return {"status": 200}

## Main
router = APIRouter(
    # prefix="/v1",
    responses={404: {"description": "Not found"}},
)


router.include_router(public_router)
# router.include_router(internal_router)
router.include_router(router_status)
