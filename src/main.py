from fastapi import FastAPI, UploadFile, HTTPException
import motor.motor_asyncio
from beanie import init_beanie
from pydantic import BaseSettings

from dotenv import load_dotenv
import os
from datetime import datetime

from .models import Transcript, TranscriptResponse
from .utils import transcribe_file, save_transcription_to_db

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


@app.get('/')
def say_hello():
    return {"hello": "there"}


@app.post('/voice-to-text')
async def handle_transcription(file: UploadFile):
    # Reject requests without a valid audio file
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 file!")

    # Get the text from the mp3 file
    try:
        transcript_text = "some new test text from goobey" 
        transcript_text = transcribe_file(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to transcribe audio. Message: {e}')

    response = await save_transcription_to_db(file, transcript_text)

    print(f"response: {response}")
    return response

