import logging

from fastapi import FastAPI
import fastapi
from route import router

logger = logging.getLogger(__name__)


app = FastAPI()

logger.info("----------APP STARTED-----------")


app.include_router(router, tags=["create"])
