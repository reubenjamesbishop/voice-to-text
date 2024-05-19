from fastapi.testclient import TestClient
from pytest_mock import mocker
from src.main import app

client = TestClient(app=app)

def test_sanity():
    """Sanity check to establish that tests are reachable by test client. 
    """
    assert True


def test_hello_route():
    """Test simple default route, ensuring that API is reachable by test client. 
    """
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {'hello': 'there'}


def test_transcribe_route(mocker): 
    """
    Test transcription happy path, uploading a known audio file and verify 
    that the transcription is as expected, in the correct format. 
    
    Note: we stub the live MongoDB interaction during testing. 
    """

    mock_resp = mocker.patch('src.main.save_transcription_to_db')
    mock_resp.return_value = {
        'id': 'abc123',
        'audio_source': './test_file.mp3',
        'content': 'A very nice transcription',
        'status': 'complete',
        'created_time': '2000-01-01 00:00:00.000000',
        'updated_time': '2000-01-01 00:00:00.000000',
    }

    file_path = './tests/media/test_file.mp3'
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "audio/mpeg")}
        resp = client.post('/voice-to-text', files=files)
        assert resp.status_code == 200


def test_transcribe_route_handle_missing_file(mocker): 
    """Test that the API is able to appropriately handle a missing file / malformed input. 
    """

    resp = client.post('/voice-to-text', files=None)
    assert resp.status_code == 422


def test_transcribe_route_handle_incorrect_file_type(mocker): 
    """Test that the API can appropriately handle incorrect types of files (e.g., images)
    """
    
    file_path = './tests/media/test_image.jpeg'
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "image/jpeg")}
        resp = client.post('/voice-to-text', files=files)
        assert resp.status_code == 400