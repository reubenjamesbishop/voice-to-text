from typing import Union
import assemblyai as aai
import os 
from typing import BinaryIO
from datetime import datetime

from .models import Transcript, TranscriptResponse

def transcribe_file(file: BinaryIO, api_key: str=os.getenv('ASSEMBLY_AI_API_KEY')) -> str:
    """
    Function to handle the transcription of mp3 audio files into text, based on the Assembly AI SDK. 
    """

    if file is None:
        raise ValueError("File is empty - please pass in a valid file.")
    
    aai.settings.api_key = api_key

    # Use AssemblyAI SDK to convert mp3 audio into text, with default config. settings. 
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    
    return transcript.text


async def save_transcription_to_db(file, transcript_text):
    """Function to handle creation and saving of Transcription documents w/ Beanie and MongoDB
    """
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