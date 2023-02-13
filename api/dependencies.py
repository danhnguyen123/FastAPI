from fastapi import Header, HTTPException
from config import config


async def get_token_header(x_token: str = Header(...)):
    if x_token != config.APP_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
