import pytest


@pytest.fixture(scope="session")
def host():
    # return 'http://82.148.19.206:8080'
    return 'http://172.20.40.128:8080'
