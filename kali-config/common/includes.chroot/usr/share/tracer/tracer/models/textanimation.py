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

__all__ = ("AsyncTextAnimation",)

from typing import Any, Callable, Generator, Tuple, Optional
from abc import ABC, abstractmethod
import asyncio

from colorama import Fore


class AbstractTextAnimation(ABC):
    @abstractmethod
    def set_condition(self, callable):
        pass

    @abstractmethod
    def set_message(self, message):
        pass

    @abstractmethod
    async def start(self):
        pass


class AsyncTextAnimation(AbstractTextAnimation):
    """Represents a simple text animation

    Attributes
    ----------
    message : str
        The message that gets displayed
    condition : Callable[..., bool]
        A callable object representing the loop condition. As
        soon as it returns `False`, the animation will stop
    args : Tuple[Any]
        Args that get passed to the condition when calling it
    colored : bool
        If the animation should be colored

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the text animation
    `len(obj)`
        Returns the length of the message

    Note
    ----
    While the animation is being displayed, there shouldn't
    be any other part in the program writing to the stdout

    Author
    ------
    chr3st5an
    """

    def __init__(
        self,
        message: str,
        condition: Callable[..., bool],
        *args,
        color: bool = True
    ):
        """Create an animation object

        Parameters
        ----------
        message : str
            The message that gets displayed
        condition : Callable[..., bool]
            A callable object representing the loop condition. As
            soon as it returns `False`, the animation will stop
        *args : Any
            Args that get passed to the condition when calling it
        color : bool, optional
            If the animation should be colored, by default True
        """

        self.set_message(message)
        self.set_condition(condition)

        self.__args = args
        self.__color = bool(color)
        self.__message = None
        self.__condition = None

    def __str__(self) -> str:
        return (f"<{self.__class__.__qualname__}(message={self.__message!r}, "
                f"condition={self.__condition}, args={self.__args}, "
                f"colored={self.__color})>")

    def __len__(self) -> int:
        return len(self.__message)

    def __await__(self) -> Generator:
        spinner_sequence = "|/-\\"

        while self.__condition(*self.__args):
            for char in spinner_sequence:
                spinner = f"[{Fore.CYAN}{char}{Fore.RESET}]" if self.colored else f"[{char}]"

                print(f"\r{spinner} {self.__message}", end="", flush=True)

                yield from asyncio.sleep(0.1).__await__()

        # Removes the loading message
        print("\r" + (" "*(len(self) + 10)), end="\r")

    @property
    def message(self) -> Optional[str]:
        return self.__message

    @property
    def condition(self) -> Optional[Callable[..., bool]]:
        return self.__condition

    @property
    def args(self) -> Tuple[Any]:
        return self.__args

    @property
    def colored(self) -> bool:
        return self.__color

    def set_message(self, message: str) -> None:
        """Assigns a new message to the animation

        Parameters
        ----------
        message : str
            The message to set for the animation object
        """

        self.__message = message

    def set_condition(self, condition: Callable[..., bool]) -> None:
        """Sets a new condition

        Parameters
        ----------
        condition : Callable[..., bool]
            A callable object representing the loop condition. As
            soon as it returns `False`, the animation will stop
        """

        self.__condition = condition

    async def start(self) -> None:
        """Displays a loading animation as long as the condition is True

        This is done by creating and awaiting an `asyncio.Task` object.
        While the animation is displayed, there shouldn't be any other
        function using `print`.
        """

        await self
