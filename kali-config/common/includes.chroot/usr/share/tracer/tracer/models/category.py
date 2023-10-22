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

from __future__ import annotations

__all__ = ("Category",)

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from copy import deepcopy


class AbstractCategory(ABC):
    @property
    @abstractmethod
    def website(self):
        pass


class Category(AbstractCategory):
    """Used to represent the category of a site

    Attributes
    ----------
    website : tracer.Website
        The website to which the category belongs to
    as_number : int
        The int representation of the category
    as_str : str
        A str containing the category name

    Classmethods
    ------------
    cls.to_number(str) -> int
        Converts the str name of a category into the
        corresponding int value
    cls.to_str(int) -> str
        Converts the int representation of a category
        into the str name of the category
    cls.all_categories() -> List[str]
        Returns a list with all available categories.

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the category
    `int(obj)`
        Alias for `obj.as_number`
    `x == obj`
        Compares the int values of both objects
    `copy.copy(obj)`
        Returns a copy of the category
    `copy.deepcopy(obj)`
        Returns a deepcopy of the category

    Author
    ------
    chr3st5an
    """

    SOCIALMEDIA = 1
    XXX = 2
    BLOG = 3
    ART = 4
    PROGRAMMING = 5
    VIDEO = 6
    MESSAGING = 7
    DATING = 8
    MUSIC = 9
    SPORT = 10
    MEMES = 11
    OFFICE = 12
    NEWS = 13
    GAMES = 14
    LINKS = 15
    OTHER = 16

    @classmethod
    def to_number(cls, category: str) -> int:
        """Returns the int representation of the given category

        Parameters
        ----------
        category : str
            The category

        Returns
        -------
        int
            The int representation of the category. -1 if the
            given category doesn't exist
        """

        return cls.__dict__.get(category.upper(), -1)

    @classmethod
    def to_str(cls, number: int) -> str:
        """Returns the str representation of the given category

        Parameters
        ----------
        number : int
            Any number

        Returns
        -------
        str
            The corresponding str representation of the number.
            "UNKNOWN" if there is no corresponding
            representation.
        """

        try:
            return [
                key for key, val in cls.__dict__.items() if val == number
            ][0]
        except IndexError:
            return "UNKNOWN"

    @classmethod
    def all_categories(cls) -> List[str]:
        """Returns a list with all categories

        Returns
        -------
        List[str]
            A list containing every category that is part
            of this class
        """

        return [attr for attr in dir(cls) if attr.isupper()]

    def __init__(
        self,
        website,
        category_number: int
    ):
        """Initializes a category

        Parameters
        ----------
        website : tracer.Website
            The website that belongs to this category
        category_number : int
            The number of the category to represent with
            this object

        Example
        -------
            >>> my_category = Category(..., Category.VIDEO)

            >>> print(my_category)  # <Category[video]>

            >>> print(my_category == Category.VIDEO)  # True
        """

        self.__website = website
        self.__number = category_number

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}[{self.as_str}]>"

    def __int__(self) -> int:
        return self.__number

    def __eq__(self, other: Any) -> bool:
        try:
            return int(self) == int(other)
        except Exception:
            return False

    def __copy__(self) -> Category:
        category = self.__class__.__new__(self.__class__)
        category.__dict__.update(self.__dict__)

        return category

    def __deepcopy__(self, memo: Dict[int, Any]) -> Category:
        category = self.__class__.__new__(self.__class__)

        memo[id(self)] = category

        for k, v in self.__dict__.items():
            setattr(category, k, deepcopy(v, memo))

        return category

    @property
    def website(self):
        return self.__website

    @property
    def as_number(self) -> int:
        return self.__number

    @property
    def as_str(self) -> str:
        return self.to_str(self.__number).lower()
