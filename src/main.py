from fastapi import FastAPI
import motor.motor_asyncio
from beanie import init_beanie
from pydantic import BaseSettings

from dotenv import load_dotenv
import os

from .models import Transcript
from .routes import router

load_dotenv()

app = FastAPI()

class Settings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_user: str = "beanie"
    mongo_pass: str = "beanie"
    mongo_db: str = "beanie_db"

    @property
    def mongo_dsn(self):
        return os.getenv('MONGO_CONNECTION_STRING')


@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(Settings().mongo_dsn)
    await init_beanie(client.beanie_db, document_models=[Transcript])
    app.include_router(router, prefix="/v1", tags=["voice-to-text"])


@app.get('/')
def say_hello():
    return {"hello": "there"}