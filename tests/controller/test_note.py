from pytest import fixture, raises, mark
from aletheophone.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestNoteController:
    @mark.asyncio
    def test_crud(self):
        response = client.post("/note", json={"text": "Hello world"})

        assert response == 200
