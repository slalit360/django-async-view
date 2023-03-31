import httpx
import pytest
from django.urls import reverse


@pytest.mark.unit
def test_async(test_client):
    url = reverse('async')
    print(url)
    response = httpx.get(url)
    assert response.status_code == 200


@pytest.mark.asyncio
def test_myapi(async_req_fac):
    url = reverse('myapi')
    response = async_req_fac.get(url)
    assert response.status_code == 200
