import asyncio

import pytest
from django.test.client import AsyncClient, AsyncRequestFactory


@pytest.fixture(scope="session")
def test_event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_client() -> AsyncClient:
    with AsyncClient() as client:
        yield client


@pytest.fixture(scope="session")
async def async_req_fac() -> AsyncRequestFactory:
    async with AsyncRequestFactory() as client:
        yield client
