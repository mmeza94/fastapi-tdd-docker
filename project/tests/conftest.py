import os

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.config import Settings, get_settings
from app.main import create_application  # updated


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


# Fixtures are reusable objects for tests. They have a scope associated with them
@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    # dependency_overrides is a dict of key/value pairs where the key is the
    # dependency name and the value is what we'd like to override it with:
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client


# new
@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client

    # tear down
