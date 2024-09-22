from os import getcwd, remove
from os.path import exists, join
from pytest import fixture
from aletheophone.config import set_config, Config


@fixture(autouse=True)
def setup_config(request):
    if request.node.get_closest_marker("db"):
        test_path = join(getcwd(), "data-test")
        db_path = join(test_path, "mg.db")

        if exists(db_path):
            remove(db_path)

        set_config(Config(storage_path=test_path, db_path=join(test_path, "mg.db")))

        yield

        if exists(db_path):
            remove(db_path)
    else:
        yield


def pytest_configure(config):
    config.addinivalue_line("markers", "db: sets up database procedures")
