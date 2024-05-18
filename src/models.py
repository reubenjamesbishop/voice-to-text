from beanie import Document
from pydantic import BaseModel

class Transcript(Document):
    audio_source: str
    content: str
    status: str
    created_time: str
    updated_time: str

    class Settings:
        collection = "transcripts"


class TranscriptResponse(BaseModel):
    id: str
    audio_source: str
    content: str
    status: str
    created_time: str
    updated_time: str
