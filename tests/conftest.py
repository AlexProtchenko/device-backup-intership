import pytest


@pytest.fixture(scope="session")
def host():
    return 'http://127.0.0.1:5000'
