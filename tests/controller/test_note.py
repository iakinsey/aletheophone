from pytest import fixture, raises, mark
from aletheophone.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestNoteController:
    def test_crud(self):
        text = "Hello world!"
        response = client.post("/note", json={"text": text})

        assert response.status_code == 200
        assert response.json()["text"] == text
