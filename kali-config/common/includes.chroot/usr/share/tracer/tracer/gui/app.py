"""
MIT License

Copyright (c) 2022 chr3st5an

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import secrets
import asyncio
import os

from aiohttp import ClientSession, DummyCookieJar, web
from aiohttp.web import Request, RouteTableDef
from jinja2 import FileSystemLoader
import aiohttp_jinja2

from tracer import (
    load_website_data,
    load_user_agent,
    WebsitePool,
    Website,
)


os.chdir(os.path.realpath(os.path.dirname(__file__)))

app = web.Application()
cookies = {}
routes = RouteTableDef()

aiohttp_jinja2.setup(
    app=app,
    enable_async=True,
    loader=FileSystemLoader("./templates")
)


@routes.get("/")
async def index(request: Request):
    """Represents the index page
    """

    return await aiohttp_jinja2.render_template_async(
        template_name="index.html",
        request=request,
        context={
            "host": request.host,
            "scheme": request.scheme,
            "pool": load_website_data()
        }
    )


@routes.post("/api/start_search")
async def start_search(request: Request):
    """Endpoint for starting a username search

    Validate data and return a searchID in form of a cookie.
    The client can now send GET requests to this endpoint
    in order to retrieve the results of the search.
    """

    username = (await request.post()).get("username", "")
    search_id = secrets.token_urlsafe(20)
    queue = asyncio.Queue()

    response = web.Response()
    response.set_cookie("search_id", search_id, max_age=300)

    cookies[search_id] = [queue, False]

    # Spawn background task
    asyncio.create_task(
        start_requests(username, queue, cookies[search_id])
    )

    return response


@routes.get("/api/start_search")
async def get_results(request: Request):
    """Endpoint for getting the results of a search

    Uses the searchID to identify the client and their
    results.
    """

    search_id = request.cookies.get("search_id", "")

    if search_id not in cookies:
        return web.Response(status=400, text="Bad Request")

    while True:
        try:
            result = await asyncio.wait_for(cookies[search_id][0].get(), 1)

            return web.json_response({"result": result})
        except asyncio.TimeoutError:
            if cookies[search_id][0].empty() and cookies[search_id][1]:
                del cookies[search_id]

                response = web.Response(text="Finished")
                response.del_cookie("search_id")

                return response


async def start_requests(
    username: str,
    queue: asyncio.Queue,
    cookie: list
) -> None:
    """Send the necessary requests

    Put the incoming responses into the given queue. This
    coro is intended to be spawned as a background task.

    Parameters
    ----------
    username : str
        Check if this username is taken
    queue : asyncio.Queue
        A queue to put the results into. Results are
        given as a list which follow this structure:
        `[username_exists : bool, url : str, delay : float]`
    cookie : list
        Cookie data assigned by `start_search` where the
        second element represents the state of this coro.
        As soon as this coro finishes, the coro changes
        the second element to `True`
    """

    headers = {"User-Agent": load_user_agent()}
    cookie_jar = DummyCookieJar()

    async with ClientSession(headers=headers, cookie_jar=cookie_jar) as session:
        pool = WebsitePool(*[
            Website.from_dict(data) for data in load_website_data()
        ])
        pool.set_username(username)

        requests = pool.start_requests(session)

        async for response in requests:
            await queue.put([
                response.successfully,
                response.url,
                response.ms
            ])

        # Finished
        cookie[1] = True


@routes.get("/favicon.ico")
async def icon(request: Request) -> web.FileResponse:
    return web.FileResponse(path="./static/assets/favicon.ico")


routes.static("/static", "./static")
app.router.add_routes(routes)
