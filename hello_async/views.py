import asyncio
import logging
from time import sleep

import httpx
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse

logger = logging.getLogger()
from request_id import generate_request_id

req_id = generate_request_id()


# helpers

async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/")
        print(r)
        # print(r.status_code)


def http_call_sync():
    for num in range(1, 6):
        sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)


# views

async def index(request):
    logger.info(req_id)
    return HttpResponse("Hello, async Django!")


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse("Non-blocking HTTP request")


def sync_view(request):
    http_call_sync()
    return HttpResponse("Blocking HTTP request")


# @sync_to_async
def sync_helper():
    print("In helper coroutine!")
    for num in range(1, 6):
        sleep(1)
        print(num)
    print("Exiting coroutine!")


async def async_helper():
    print("In helper coroutine!")
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    print("Exiting coroutine!")


# custom done callback function
def callback(task):
    # report a message
    print('Task is done')


async def translate(request: ASGIRequest):
    logger.info(req_id)
    loop = asyncio.get_event_loop()  # each thread got its own event loop
    if request.method in {'GET', 'POST'}:
        # HELP: below script is to convert sync to sync
        # async_helper_converted = sync_to_async(sync_helper, thread_sensitive=False)
        # await loop.create_task(async_helper_converted())
        #       OR
        task = loop.create_task(async_helper())
        task.add_done_callback(callback)
        return HttpResponse(f"{request.method.upper()} -> Health is okay")

    return HttpResponse("status=500")
