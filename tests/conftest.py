import pytest


@pytest.fixture
def test_client():
    import person_service.app as app
    test_app = app.create_app()
    client = test_app.test_client()
    yield client
