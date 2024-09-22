from json import loads
from os import getcwd
from os.path import join
from aletheophone.app import app
from fastapi.testclient import TestClient

AUDIO_FILE = join(getcwd(), "data-test", "quickbrownfox.mp3")
EXPECTED_TEXT = "The quick brown fox jumps over the lazy dog."


class TestStreamController:
    def test_stream(self):
        client = TestClient(app)
        with client.websocket_connect("/stream") as conn:
            conn.send_bytes(open(AUDIO_FILE, "rb").read())
            conn.send_bytes("b\x9E\x84")

            payload = conn.receive_json()

            assert payload["id"] is not None
            assert payload["text"] == EXPECTED_TEXT
