from src.AudioTranscriber import AudioTranscriber, transcribe_file

def test_audio_transcriber():
    AudioTranscriber()
    assert True

def test_transcribe_file():
    """Test that the transcribe function works on a known case.
    """
    with open('./tests/test_file.mp3', "rb") as file:
        r = transcribe_file(file)
        assert r == 'Thanks. Connecting you now.'