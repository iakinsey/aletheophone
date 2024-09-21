from os import getcwd, remove
from os.path import exists, join
from pytest import fixture
from aletheophone.app import app
from aletheophone.config import set_config, Config
from fastapi.testclient import TestClient


@fixture(autouse=True)
def setup_config():
    test_path = join(getcwd(), "data-test")
    db_path = join(test_path, "mg.db")

    if exists(db_path):
        remove(db_path)

    set_config(Config(storage_path=test_path, db_path=join(test_path, "mg.db")))

    yield

    if exists(db_path):
        remove(db_path)


class TestNoteController:
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
