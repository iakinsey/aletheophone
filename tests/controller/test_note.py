from fastapi.testclient import TestClient
from pytest import mark

from aletheophone.app import app


class TestNoteController:
    @mark.db
    def test_crud(self):
        client = TestClient(app)
        text = "Hello world!"
        response = client.post("/note", json={"text": text})

        assert response.status_code == 200

        json = response.json()

        assert json["text"] == text

        response = client.get(f"/note/{json['id']}")

        assert response.json()["id"] == json["id"]

        response = client.get(f"/notes")
        notes = response.json()

        assert len(notes) == 1

        response = client.delete(f"/note/{json['id']}")

        assert response.status_code == 200

        response = client.get(f"/note/{json['id']}")

        assert response.status_code == 404

        response = client.get(f"/notes")
        notes = response.json()

        assert len(notes) == 0
