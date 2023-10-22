#!/usr/bin/env python3

"""Tracer

This script allows to detect on which websites a username is currently
taken. Chances are that there is always the same person behind a username as
long as the username is special enough.

Arguments can be provided through the CLI or through the config (.conf) file.

Dependencies: requirements.txt
"""

__all__ = ("Tracer",)

from typing import Dict, List, Optional, Union
from threading import Thread
from time import monotonic
from pathlib import Path
import http.cookies
import webbrowser
import asyncio
import json
import os

from pyvis.network import Network
from aiohttp import ClientSession
from aiohttp.web import run_app
from colorama import Fore
import aiohttp

from models import *
from loader import *


CONFIG = "../settings.conf"
MY_IP = "https://api.myip.com"


class Tracer(object):
    """Implement the main logic behind Tracer

    Author
    ------
    chr3st5an
    """

    @classmethod
    def main(cls) -> None:
        """Create a tracer instance and call its run coro

        Parse given args and create an event loop
        which executes the `run` coro
        """

        # Changing dir so that relative paths make sense
        os.chdir(os.path.dirname(__file__))

        # Parse the configs from the conf file and
        # update these with the arguments given by the CLI
        kwargs = TracerParser(CONFIG).parse()

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if kwargs.get("web"):
                from gui import app

                loop.call_later(1, webbrowser.open, "http://127.0.0.1:12345")
                run_app(app, host="127.0.0.1", port=12_345, loop=loop)
            else:
                loop.run_until_complete(cls(kwargs.pop("username"), **kwargs).run())
        except KeyboardInterrupt:
            print("👋 Bye")
        finally:
            loop.stop()

    def __init__(
        self,
        username: str,
        data: Optional[List[Dict[str, str]]] = None,
        user_agent: Optional[str] = None,
        **kwargs,
    ):
        if data is None:
            data = load_website_data()

        if user_agent is None:
            user_agent = load_user_agent()

        self.username = username
        self.kwargs = dict(kwargs)
        self.user_agent = user_agent
        self.verbose = kwargs.get("verbose", False)
        self.pool = WebsitePool(*[Website.from_dict(data_) for data_ in data])

        self.pool.set_username(self.username)

        self._out_dir = None
        self.__filter_sites()

        if kwargs.get("create_file_output"):
            self._create_output_dir()

        # When sending a request to TikTok, an annoying message
        # is printed by aiohttp. This turns the message off.
        http.cookies._is_legal_key = lambda _: True

    def __str__(self) -> str:
        return (
            f"<{self.__class__.__qualname__}(username={self.username!r}, "
            f"kwargs={self.kwargs}, pool={self.pool})>"
        )

    def __filter_sites(self) -> None:
        """Filter the list of sites based on the given arguments"""

        include: List[str] = self.kwargs.get("only", []) + self.kwargs.get(
            "only_category", []
        )

        exclude: List[str] = self.kwargs.get("exclude", []) + self.kwargs.get(
            "exclude_category", []
        )

        if not (include or exclude):
            return None

        if exclude:
            self.pool.remove(
                lambda w: (w.domain in exclude) or (w.category.as_str in exclude)
            )

        if include:
            self.pool.remove(
                lambda w: not ((w.domain in include) or (w.category.as_str in include))
            )

    async def run(self) -> None:
        """Run the program"""

        if self.kwargs.get("print_logo", True):
            print(f"\n{Fore.CYAN}{load_logo()}{Fore.RESET}\n")

        cookie_jar = aiohttp.DummyCookieJar()
        headers = {"User-Agent": self.user_agent}

        async with ClientSession(headers=headers, cookie_jar=cookie_jar) as session:
            if self.kwargs.get("ip_check"):
                await self.retrieve_ip(
                    session=session, timeout=self.kwargs.get("ip_timeout")
                )

            print(f"[{Fore.CYAN}*{Fore.RESET}] Checking {Fore.CYAN}{self.username}"
                  f"{Fore.RESET} on {len(self.pool)} sites:\n")

            start = monotonic()
            counter = 0
            requests = self.pool.start_requests(session, self.kwargs.get("timeout"))

            async for response in requests:
                message = f"{response.url} {response.verbose() if self.kwargs.get('verbose') else ''}"

                if not response.successfully:
                    if self.kwargs.get("all"):
                        if response.timeout:
                            print(f"{Fore.RED}[Timeout]{Fore.RESET} {message}")
                        else:
                            print(f"{Fore.RED}[-]{Fore.RESET} {message}")

                    continue

                print(f"{Fore.GREEN}[+]{Fore.RESET} {message}")

                if self.kwargs.get("browse"):
                    Thread(target=webbrowser.open, args=(response.url,)).start()

                counter += 1

        print(f"\n[{Fore.CYAN}={Fore.RESET}] Found {Fore.CYAN}{counter}"
              f"{Fore.RESET} match(es) in {Fore.CYAN}{monotonic() - start:.2f}"
              f"s{Fore.RESET}")

        self.write_report(self._out_dir)
        self.draw_graph(self._out_dir)

    def write_report(self, out_dir: Union[str, Path]) -> None:
        """Create and write a report file which contains the results

        Parameters
        ----------
        out_dir : Union[str, Path]
            In which directory to save the report file. If `None`
            is given, then no report file is created
        """

        if self._out_dir is None:
            return None

        name = f"{out_dir}result.txt"
        mode = "w" if os.path.exists(name) else "x"

        with open(name, mode) as file:
            file.write(f"{load_logo()}\nReport for {self.username}:\n\n")

            for result in self.pool.results:
                file.write(result.url + "\n")

        return None

    def draw_graph(self, out_dir: Optional[Union[str, Path]]) -> None:
        """Visualize the results

        Create a HTML file containing a graph and open it
        in the default webbrowser

        Parameters
        ----------
        out_dir : Union[str, Path]
            In which directory to save the HTML file. If `None`
            is given, then no graph is created
        """

        if self._out_dir is None:
            return None

        net = Network(
            height="100%",
            width="100%",
            bgcolor="#282a36",
            font_color="#f8f8f2",
        )

        net.add_node(self.username, color="#ff79c6", title="Username", shape="circle")

        for category in Category.all_categories():
            net.add_node(
                n_id=category.title(),
                color="#bd93f9",
                shape="circle",
                title=category.title(),
                labelHighlightBold=True,
            )
            net.add_edge(self.username, category.title())

        for site in self.pool:
            if site.result.user_exists:
                net.add_node(
                    n_id=site.name,
                    color="#ff5555",
                    shape="circle",
                    title=site.url,
                    labelHighlightBold=True,
                )
                net.add_edge(site.category.as_str.title(), site.name)

        # Settings for the graph
        net.toggle_physics(True)
        net.set_edge_smooth("dynamic")

        # Save the graph in a html file and open it
        # in the default browser
        net.show(f"{out_dir}graph.html")

        return None

    async def retrieve_ip(
        self,
        session: ClientSession,
        timeout: Optional[float] = None
    ) -> None:
        """Retrieve the IP address and prints it

        Sleep for 3 seconds after the IP got retrieved.

        Parameters
        ----------
        session : aiohttp.ClientSession
            Session used to send a request
        timeout : Union[int, float], optional
            Set a timeout for the request, by default None
        """

        async def send_request() -> Dict[str, str]:
            timeout_ = aiohttp.ClientTimeout(timeout)

            try:
                async with session.get(MY_IP, timeout=timeout_) as r:
                    return json.loads(await r.text())
            except asyncio.TimeoutError:
                return {"ip": "0.0.0.0 [TIMEOUT]"}

        response = asyncio.create_task(send_request())

        await AsyncTextAnimation("Retrieving IP...", lambda: not response.done())

        print(f"Your IP address is {Fore.CYAN}{response.result()['ip']}{Fore.RESET}\n")

        await asyncio.sleep(3)

    def _create_output_dir(self) -> None:
        """Create the directory in which the results are saved"""

        results_dir = "../results/"

        if not os.path.exists(results_dir):
            try:
                os.mkdir(results_dir)
            except PermissionError:
                return None

        if not os.path.exists(f"{results_dir}{self.username}"):
            os.mkdir(f"{results_dir}{self.username}/")

        self._out_dir = f"{results_dir}{self.username}/"


if __name__ == "__main__":
    Tracer.main()
