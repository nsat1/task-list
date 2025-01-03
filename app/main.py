import logging
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from api import router as api_router
from core.models import db_helper


logging.basicConfig(level=logging.INFO, format=settings.logging.log_format)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
