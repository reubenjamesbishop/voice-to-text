from typing import Union
import assemblyai as aai
import os 
from typing import BinaryIO

class AudioTranscriber:

    def __init__(self) -> None:
        aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
        self.transcriber = aai.Transcriber()

    def transcribe_file(self, file: Union[BinaryIO, str]):
        transcript = self.transcriber.transcribe(file)
        return transcript.text




# # transcript_text = transcribe_file(file.file)
# def transcribe_file(file):
#     aai.settings.api_key = os.getenv('ASSEMBLY_AI_API_KEY')
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(file)
#     return transcript.text
