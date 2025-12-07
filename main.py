import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Code Generation Chatbot")

    settings = get_settings()
    if not settings.AWS_REGION:
        logger.warning("AWS_REGION not set, default region will be used")
    if not settings.MODEL_ID:
        logger.warning("MODEL_ID not set, default model will be used")

    yield

    logger.info("Shutting down Code Generation Chatbot")


app = FastAPI(title="Code Generation Chatbot", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
