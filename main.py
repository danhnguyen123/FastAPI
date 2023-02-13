from dotenv import load_dotenv
load_dotenv()

import uvicorn, time
from uvicorn.config import LOGGING_CONFIG

from fastapi import FastAPI, Request, Depends

from api.router import router as main_router

from api.dependencies import get_query_token, get_token_header

from config import config
from api import router
from metadata import app_description,tags_metadata, contact_metadata

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    # dependencies=[Depends(get_token_header)],
    openapi_tags = tags_metadata,
    description=app_description,
    contact=contact_metadata
)

origins = ["http://localhost", f"http://localhost:{config.API_HOST_PORT}",]
app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(main_router)

## add middleware return process time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

from typing import Union

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    # log_config = uvicorn.config.LOGGING_CONFIG
    # log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run('main:app'
            ,host= config.API_HOST_DOMAIN
            ,port= config.API_HOST_PORT
            ,reload = config.RELOAD_CODE
            ,workers = config.NUMBER_OF_WORKER
            # , log_config=log_config
            )
