import pytest

@pytest.fixture(scope="class")
def db_class(request):
    class DummyDB:
        pass

    request.cls.db = DummyDB()