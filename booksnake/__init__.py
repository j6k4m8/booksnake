import urllib

#!/usr/bin/env python3

"""
The main driver for booksnake.

Download some delicious reads!
"""


from typing import List, Union

import os.path
import json
import io
import sys

import requests
from libgen_api import LibgenSearch

# import pandas as pd
import bs4 as bs

from .sending import send_file

SUPPORTED_EXTENSIONS = ["mobi", "azw", "text", "txt", "epub", "rtf"]
SUPPORTED_LANGUAGES = ["english"]


class Book:
    def __init__(self, title: str, author: str, ext: str) -> None:
        """ """
        self.title = title
        self.author = author
        self.ext = ext

    def download(self, destination: str) -> Union[str, io.BytesIO]:
        ...

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "ext": self.ext,
        }


class Searcher:
    def __init__(self) -> None:
        """ """

    def search(self, query: str) -> List[Book]:
        ...


class LibgenBook(Book):
    def __init__(
        self, title: str, author: str, ext: str, mirrors: List[str], data: dict = None
    ) -> None:
        self.title = title
        self.author = author
        self.ext = ext
        self.mirrors = mirrors
        self._data = data

    @staticmethod
    def from_dict(data: dict):
        return LibgenBook(
            title=data.get("Title", data.get("title")),
            author=data.get("Author", data.get("author")),
            ext=data.get("Extension", data.get("ext")),
            mirrors=data.get("links", None)
            or [v for k, v in data.items() if "Mirror" in k],
            data=data,
        )

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "ext": self.ext,
            "links": self.mirrors,
            "data": self._data,
            "type": "LibgenBook",
        }

    def __repr__(self) -> str:
        return f'<LibgenBook "{self.title}" by {self.author}>'

    def __str__(self):
        return self.__repr__()

    def download(self, destination: str = None) -> Union[str, io.BytesIO]:
        for mirror in self.mirrors:
            try:
                content = requests.get(mirror).content
                soup = bs.BeautifulSoup(content, "lxml")
                download_link = soup.find_all("a", text="GET")[0]["href"]
                book_contents = requests.get(download_link).content
                if destination:
                    with open(destination, "wb") as fh:
                        fh.write(book_contents)
                    return
                else:
                    return book_contents
            except:
                pass
        raise ValueError("Could not download from any provided mirrors.")


class LibgenSearcher(Searcher):
    def __init__(self) -> None:
        super().__init__()

    def search(self, query: str) -> List[Book]:
        try:
            res = LibgenSearch().search_title(query)
        except IndexError:
            return []
        return [
            LibgenBook.from_dict(r)
            for r in res
            if (
                r["Extension"].lower() in SUPPORTED_EXTENSIONS
                and r["Language"].lower() in SUPPORTED_LANGUAGES
            )
        ]


# class LibgenFictionSearcher(Searcher):
#     def __init__(self, base_url: str = "http://libgen.is/fiction/") -> None:
#         self.base_url = base_url

#     def search(self, query: str) -> List[Book]:

#         f = requests.get(f"{self.base_url}?q={query}").content
#         soup = bs.BeautifulSoup(f, "lxml")
#         parsed_table = soup.find_all("table")[0]
#         data = [
#             [
#                 # {tag.text.split(" ")[0]: tag["href"] for tag in td.find_all("a")}
#                 # if td.find_all("a")
#                 # else
#                 "".join(td.stripped_strings).replace("&varr;", "")
#                 for td in row.find_all("td")
#             ]
#             for row in parsed_table.find_all("tr")
#         ]
#         table = pd.DataFrame(data[1:], columns=data[0])


#         unfiltered_results = [
#             LibgenBook(
#                 title="".join(row.Title.keys()),
#                 author=(
#                     row["Author(s)"]
#                     if isinstance(row["Author(s)"], str)
#                     else "".join(row["Author(s)"].keys())
#                 ),
#                 ext=row["File"].split("/")[0].lower().strip(),
#                 mirrors=list(row["Mirrors"].values()),
#                 data=dict(row),
#             )
#             for _, row in table.iterrows()
#         ]
#         return [
#             book
#             for book in unfiltered_results
#             if (
#                 book.ext in SUPPORTED_EXTENSIONS
#                 and book._data["Language"].lower() in SUPPORTED_LANGUAGES
#             )
#         ]


class GutenbergBook(Book):
    def __init__(self, author, title, ext, link, data: dict = None) -> None:
        self.author = author
        self.title = title
        self.ext = ext
        self.link = link
        self._data = data

    def __repr__(self) -> str:
        return f'<GutenbergBook "{self.title}" by {self.author}>'

    def __str__(self):
        return self.__repr__()

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "ext": self.ext,
            "links": [self.link],
            "data": self._data,
            "type": "GutenbergBook",
        }

    @staticmethod
    def from_dict(data: dict) -> Book:
        return GutenbergBook(
            author=data["author"],
            title=data["title"],
            ext=data["ext"],
            link=data["link"],
            data=data["data"],
        )

    def download(self, destination: str = None) -> Union[str, io.BytesIO]:
        book_content = requests.get(self.link).content
        if destination:
            with open(destination, "wb") as fh:
                fh.write(book_content)
            return
        else:
            return book_content


class GutenbergSearcher(Searcher):
    """
    Searches Project Gutenberg
    """

    def __init__(self):
        self.base_url = "https://www.gutenberg.org"

    def search(self, query):
        query = query.replace(" ", "+")
        query = "/ebooks/search/?query=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        try:
            content = f.read()
        except Exception:
            Warning(
                "You've probably hit the Gutenberg page too many times "
                + "and have been banned for 24 hours by their rate-limiter. "
            )
            return []
        soup = bs.BeautifulSoup(content, "html.parser")
        links = soup.findAll("li", {"class": "booklink"})
        options = []
        for a in links:
            author = a.find("span", {"class": "subtitle"})
            author = author.text.strip() if author else " "
            title = a.find("span", {"class": "title"}).text.strip()

            options.append(
                GutenbergBook(
                    author=author,
                    title=title,
                    ext="mobi",
                    link=self.base_url + (a.find("a").get("href") + ".kindle.images"),
                )
            )
        return options


DEFAULT_SEARCHERS = [
    (GutenbergSearcher, ()),
    (LibgenSearcher, ()),
    # (LibgenFictionSearcher, ()),
]


def cli():
    def _cli_list(query) -> List[Book]:
        results = []
        for searcher, args in DEFAULT_SEARCHERS:
            try:
                results = [*results, *searcher(*args).search(query)]
            except Exception as e:
                print(f"Error in {searcher}: {e}")

        for i, result in enumerate(results):
            print(f"{i+1}:\t{result}")
        return results

    def _interactive_search(query) -> Book:
        results = _cli_list(query)

        selection = input("> ")
        if selection.isnumeric():
            selection = int(selection)
            if selection > 0 and selection <= len(results):
                return results[selection - 1]
        else:
            print("Quitting...")

    def _cli_download(query):
        book = _interactive_search(query)
        book.download(book.title + "." + book.ext)

    def _cli_search(query):
        _cli_list(query)

    def _cli_send(query):
        book = _interactive_search(query)
        contents = io.BytesIO(book.download())
        contents.seek(0)
        send_file(
            filename=book.title + "." + book.ext,
            contents=contents,
            settings=json.load(
                open(os.path.expanduser("~/.config/booksnake.json"), "r")
            ),
        )

    def _cli_fail(query):
        print("Something went wrong. Try booksnake [download|search|send] QUERY")

    commands = {
        "download": _cli_download,
        "search": _cli_search,
        "send": _cli_send,
    }

    command = sys.argv[1]
    query = " ".join(sys.argv[2:])

    commands.get(command, _cli_fail)(query)


if __name__ == "__main__":
    cli()
