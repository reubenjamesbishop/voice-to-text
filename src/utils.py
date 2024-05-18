from typing import Union
import assemblyai as aai
import os 
from typing import BinaryIO

def transcribe_file(file: BinaryIO, api_key: str=os.getenv('ASSEMBLY_AI_API_KEY')) -> str:
    """
    Function to handle the transcription of mp3 audio files into text, based on the Assembly AI SDK. 
    """
    
    aai.settings.api_key = api_key

    # Use AssemblyAI SDK to convert mp3 audio into text, with default config. settings. 
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file)
    
    return transcript.text