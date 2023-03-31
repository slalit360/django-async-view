import pytest


@pytest.mark.asyncio
async def test_sync(client):
    response = await client.get("/sync/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_async(client):
    response = await client.get("/async/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_my_api(client):
    response = await client.get("/myapi/")
    assert response.status_code == 200
