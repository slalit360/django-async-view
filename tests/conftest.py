import asyncio

import pytest
from django.test.client import AsyncClient


@pytest.fixture(scope="session")
def test_event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client() -> AsyncClient:
    yield AsyncClient()
