from src.utils import transcribe_file

def test_sanity():
    """Sanity check to establish that tests are reachable by test client. 
    """
    assert True

def test_transcribe_file():
    """Test that the transcribe function works on a known case.
    """
    with open('./tests/media/test_file.mp3', "rb") as file:
        r = transcribe_file(file)
        assert r == 'Thanks. Connecting you now.'

def test_transcribe_file_no_input():
    """Test that the transcribe function raises the apprioriate exception if the file is missing.
    """

    try: 
        transcribe_file(file=None)
    except ValueError as e:
        assert True
    except:
        assert False