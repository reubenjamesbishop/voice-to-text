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


@app.on_event("startup")
async def app_init():
    """Initialise a mongoDB connection w/ Beanie when the FastAPI server is first initialised. 
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_CONNECTION_STRING'))    
    await init_beanie(client.beanie_db, document_models=[Transcript])


@app.get('/')
def send_greeting():
    """Simple default endpoint to check that the API server is up and running. 
    """
    return {"message": "hello world"}


@app.post('/voice-to-text')
async def handle_transcription(file: UploadFile):
    """Route to handle transcription of posted mp3 audio files into text, and log transcription
    documents and metadata in the accompanying MongoDB database.
    """

    # Reject requests without a valid audio file
    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 file!")

    # Get the text from the mp3 file
    try:
        transcript_text = transcribe_file(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to transcribe audio. Message: {e}')

    # Save the transcription document in the MongoDB collection
    try: 
        response = await save_transcription_to_db(file, transcript_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to save transcription in DB. Message: {e}')

    print(f"response: {response}")
    return response

