from pytest import fixture, raises, mark
from aletheophone.app import app
from fastapi.testclient import TestClient


class TestNoteController:
    def test_crud(self):
        client = TestClient(app)
        text = "Hello world!"
        response = client.post("/note", json={"text": text})

        assert response.status_code == 200

        json = response.json()

        assert json["text"] == text

        response = client.get(f"/note/{json['id']}")

        print(response)
