from typing import Union
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
from pydantic import BaseModel
import os

import assemblyai as aai

load_dotenv()

app = FastAPI()

@app.post("/voice-to-text")
def create_transcription(file: UploadFile): 

    print(file.content_type)
    print(file.filename)

    aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file.file)

    return {"transcription": transcript.text}


