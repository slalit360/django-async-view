import asyncio
import logging
from asyncio import Future
from time import sleep

import httpx
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse

logger = logging.getLogger()

urls = ["https://httpbin.org/status/200", "https://httpbin.org/get"]


# helpers

async def http_call_async(url):
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(f"{url} -> ", num)
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print(f"{url} -> ", r)


def http_call_sync():
    for num in range(1, 6):
        sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)


# views

async def index(request):
    return HttpResponse("Hello, async Django!")


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async(urls[0]))
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
    logger.info("In myapi helper coroutine!")
    for num in range(1, 6):
        await asyncio.sleep(1)
        logger.info(num)
    logger.info("Exiting myapi coroutine!")


# custom done callback function
def callback_myapi(tasks: Future):
    logger.info(f'API Callback -> Task is {tasks._state}')


async def myapi(request: ASGIRequest):
    logger.info("In MyAPI")
    loop = asyncio.get_event_loop()  # each thread got its own event loop
    if request.method in {'GET', 'POST'}:
        # HELP: below script is to convert sync to sync
        # async_helper_converted = sync_to_async(sync_helper, thread_sensitive=False)
        # await loop.create_task(async_helper_converted())
        #       OR
        task = loop.create_task(async_helper())
        task.add_done_callback(callback_myapi)
        return HttpResponse(f"{request.method.upper()} -> Health is okay")

    return HttpResponse("status=500")


def callback_http(tasks: Future):
    logger.info(tasks)
    logger.info(f'HTTP Callback -> Task is {tasks._state}')


async def myapi_io(request: ASGIRequest):
    logger.info("In HTTP Api")
    if request.method in {'GET', 'POST'}:
        resps: Future = asyncio.gather(*map(http_call_async, urls))
        print(resps.add_done_callback(callback_http))
        return HttpResponse(f"{request.method.upper()} -> Health is okay")

    return HttpResponse("status=500")
