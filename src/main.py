from typing import Union, Optional
from fastapi import FastAPI, UploadFile, HTTPException
from dotenv import load_dotenv
from beanie import Document
from pydantic import BaseModel
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from beanie import Document, Indexed, init_beanie
import os
import assemblyai as aai
from contextlib import asynccontextmanager
from pydantic import BaseSettings
from datetime import datetime

from .models import Transcript, TranscriptResponse

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


def transcribe_file(file):
    aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    return transcript.text


@app.post("/voice-to-text", tags=['voice-to-text'], response_model=TranscriptResponse)
async def create_transcription(file: UploadFile): 

    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 file!")

    # transcript_text = transcribe_file(file.file)
    transcript_text: str = "some new test text"  
    
    current_time: datetime = datetime.now()
    t = Transcript(
        audio_source=file.filename,
        content=transcript_text,
        status="complete",
        created_time=f"{current_time}",
        updated_time=f"{current_time}",
    )
    await t.create()

    response = TranscriptResponse(
        id=str(t.id),
        audio_source=t.audio_source,
        content=t.content,
        status=t.status,
        created_time=t.created_time,
        updated_time=t.updated_time,
    )

    return response




