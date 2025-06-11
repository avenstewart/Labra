import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext

BASE_URL = "https://callook.info/"

@pytest.fixture(scope="session")
def base_config():
    return {
        "base_url": BASE_URL,
        "timeout": 15
    }

@pytest.fixture(scope="session")
def nav_pages():
    return [
        {"home": "/"}
    ]

@pytest.fixture(scope="session")
def api_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Accept": "application/json"
        }
    )
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def callsigns():
    return {
        "VALID": {"callsign": "KG5AFV", "type": "PERSON", "class": "TECHNICIAN"},
        "INVALID": {"callsign": "ABCD"}
    }