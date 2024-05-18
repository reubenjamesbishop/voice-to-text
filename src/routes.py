from fastapi import UploadFile, HTTPException, APIRouter
from datetime import datetime
import logging

from .models import Transcript, TranscriptResponse
from .AudioTranscriber import AudioTranscriber

router = APIRouter()

@router.post("/voice-to-text", tags=['voice-to-text'], response_model=TranscriptResponse)
async def create_transcription(file: UploadFile): 

    if file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 file!")

    try:
        transcript_text = AudioTranscriber().transcribe_file(file.file) 
        # transcript_text = "some new test text" 
    except Exception as e:
        print(f'Failed to transcribe audio. Message: {e}')
    
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
