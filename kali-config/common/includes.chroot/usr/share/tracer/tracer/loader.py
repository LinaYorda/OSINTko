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

__all__ = ("load_logo", "load_user_agent", "load_website_data")

from typing import Any, Callable, Dict, List
from functools import wraps
import secrets
import json
import os

from colorama import Fore


DATA_FOLDER = "../data/"


def dir_switcher(__func: Callable[..., Any], /) -> Callable[..., Any]:
    """Helper for switching working dirs

    Switch the working directory to the directory
    that contains this file and execute the given
    function. After execution, switch back to the
    original working directory.

    This is necessary for relative paths to work.
    """

    @wraps(__func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        origin = os.getcwd()
        os.chdir(os.path.dirname(__file__))

        result = __func(*args, **kwargs)

        return os.chdir(origin) or result

    return wrapper


@dir_switcher
def load_logo() -> str:
    try:
        with open(f"{DATA_FOLDER}logo.txt") as file:
            return file.read()
    except FileNotFoundError:
        return "<DEFAULT LOGO>"


@dir_switcher
def load_user_agent() -> str:
    try:
        with open(f"{DATA_FOLDER}user_agents.json") as file:
            user_agents: List[str] = json.load(file)

            return secrets.choice(user_agents)
    except FileNotFoundError:
        return "Tracer/1.0 (+https://github.com/chr3st5an/tracer)"


@dir_switcher
def load_website_data() -> Dict[str, str]:
    try:
        with open(f"{DATA_FOLDER}pool.json") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Fore.RED}[ISSUE] Couldn't find the website data "
              f"file!{Fore.RESET}")
        exit(1)
