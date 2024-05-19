from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from bson import ObjectId
import pytest 

from pytest_mock import mocker

from datetime import datetime

from src.main import app
from src.models import Transcript


client = TestClient(app=app)

def test_sanity():
    assert True


def test_hello_route():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {'hello': 'there'}


def test_transcribe_route(mocker): 

    thing = mocker.patch('src.main.save_transcription_to_db')
    thing.return_value = {
        'id': 'abc123',
        'audio_source': './test_file.mp3',
        'content': 'A very nice transcription',
        'status': 'complete',
        'created_time': '2000-01-01 00:00:00.000000',
        'updated_time': '2000-01-01 00:00:00.000000',
    }

    file_path = './tests/test_file.mp3'
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "audio/mpeg")}
        resp = client.post('/voice-to-text', files=files)
        assert resp.status_code == 200
