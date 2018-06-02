"""
Booksnake v 0.3.0.

@j6k4m8
"""

import re
import urllib
import urllib.request
import time

from typing import List

from bs4 import BeautifulSoup
import requests

from .printing import pretty_format, pretty_print, RED, YELLOW, BLUE, GREEN, BOLD, PURPLE, UNDERLINE


__version__ = "0.3.0"


def _attempt_url(url, fmt: str = "mobi", fname: str=None):
    """
    Attempt to download a file. Returns `None` if the download fails.

    Arguments:
        url (str): The url to attempt
        fmt (str : 'mobi'): The format of the downloaded asset, if known
        fname (st : None): The filename to which the file should be saved

    Returns:
        str: The filename of the downloaded file

    """
    if fname is None:
        # Make up your own name:
        filename = ".booksnake_{}.{}".format(str(int(time.time())), fmt)
    else:
        # A name was specified, use that:
        filename = "{}.{}".format(fname.strip(), fmt)
    filename, _ = urllib.request.urlretrieve(url, filename)
    return filename

class Result:
    """
    A result contains the information that points to a book download URL.

    It also contains information like title, format, and author.
    """

    def __init__(self, url, size, fmt, title, author, source="Unknown"):
        """
        Create a new result.

        Populate 1-to-1 with variable names
        """
        self.url = url
        self.size = size
        self.fmt = fmt
        self.title = title
        self.author = author
        self.source = source


class Searcher:

    def __init__(self):
        self.base_url = ""

    def url(self, suffix=""):
        """
        Generate a URL for this searcher.

        .
        """
        return "{}/{}".format(self.base_url, suffix)

    def search(self, query):
        raise NotImplementedError()

    def download(self, result: 'Result'):
        return _attempt_url(result.url)


class ManyBooksSearcher(Searcher):
    """
    Searches www.manybooks.net
    """

    def __init__(self):
        self.base_url = "http://www.manybooks.net"

    def search(self, query):
        query = query.replace(' ', '+')
        query = "/search.php?search=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        entries = soup.find_all('div', class_=["row", "grid_12"])
        options = [Result(
            author=re.findall("<br/>by (.*)", str(a))[0],
            title=a.find_all("a")[0].text,
            fmt="azw",
            url="{}/send/1:kindle:.azw:kindle/{}/{}.azw".format(
                self.base_url, *[
                    a.find_all('a')[0].attrs['href']
                    .replace(".html", "")
                    .replace("/titles/", "")
                ] * 2),
            size=None,
            source="ManyBooks"
        ) for a in entries]
        return options


class GutenbergSearcher(Searcher):
    """
    Searches Project Gutenberg
    """

    def __init__(self):
        self.base_url = "https://www.gutenberg.org"

    def search(self, query):
        query = query.replace(' ', '+')
        query = "/ebooks/search/?query=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        try:
            content = f.read()
        except Exception:
            pretty_print([RED, UNDERLINE], "RATE LIMITED!")
            pretty_print(
                [YELLOW],
                "You've probably hit the Gutenberg page too many times " +
                "and have been banned for 24 hours by their rate-limiter. "
            )
            return []
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.findAll("li", {"class": "booklink"})
        options = []
        for a in links:
            author = a.find('span', {
                'class': 'subtitle'
            })
            author = author.text.strip() if author else " "
            title = a.find('span', {
                'class': 'title'
            }).text.strip()

            options.append(Result(
                author=author,
                title=title,
                fmt='mobi',
                url=self.url(
                    a.find('a').get('href') +
                    ".kindle.images"
                ),
                size=' ',
                source="Gutenberg"
            ))
        return options


class LibGenSearcher(Searcher):
    """
    Searches libgen.io
    """

    def __init__(self):
        self.ff_base_url = (
            "http://libgen.io" +
            "/foreignfiction/index.php?" +
            "s={}&f_lang=English&f_columns=0&f_ext=All"
        )
        self.sci_base_url = (
            "http://libgen.io" +
            "/search.php?" +
            "req={}"
        )

    def _ff_options(self, query):
        content = requests.get(self.ff_base_url.format(query)).text
        soup = BeautifulSoup(content, 'html.parser')
        options = []
        for a in soup.findAll('table')[-1].findAll('tr'):
            try:
                link = a.findAll('a')[-2].get('href').replace(
                    'ads.php', 'get.php'
                )

                if link[0] == "/":
                    link = "http://libgen.io" + link

                link = BeautifulSoup(
                    requests.get(link).text, 'html.parser'
                ).findAll('a')[-1].get('href')

                size = "   "
                try:
                    size = re.findall(
                        r".*\((.*)\).*",
                        a.findAll('td')[-1].text.strip()
                    )[0]
                except Exception:
                    pass
                options.append(Result(
                    url=link,
                    size=size,
                    fmt=a.findAll('td')[-1].text.strip().split('(')[0],
                    title=(
                        a.findAll('td')[1].text.strip() +
                        " " +
                        a.findAll('td')[2].text.strip()
                    ),
                    author=a.findAll('td')[0].text.strip(),
                    source="LibGen"
                ))
            except Exception:
                pass
        return options

    def _sci_options(self, query):
        content = requests.get(self.sci_base_url.format(query)).text
        soup = BeautifulSoup(content, 'html.parser')
        options = []
        for a in soup.findAll('table')[2].findAll('tr')[1:]:
            try:
                link = [
                    ll for ll in a.findAll('a')
                    if 'ads.php' in ll.get('href', '')
                ][0].get('href').replace(
                    'ads.php', 'get.php'
                )

                if link[0] == "/":
                    link = "http://libgen.io" + link

                content = requests.get(link).text
                soup = BeautifulSoup(content, 'html.parser')
                link = [
                    a for a in soup.findAll('a')
                    if 'get.php' in a.get('href')
                ][0].get('href')

                size = "   "
                try:
                    size = re.findall(
                        r".*\((.*)\).*",
                        a.findAll('td')[-1].text.strip()
                    )[0]
                except Exception as exc:
                    pass
                options.append(Result(
                    url=link,
                    size=a.findAll('td')[7].text.strip(),
                    fmt=a.findAll('td')[8].text.strip(),
                    title=(
                        a.findAll('td')[2].text.strip()
                    ),
                    author=a.findAll('td')[1].text.strip(),
                    source="LibGen"
                ))
            except Exception:
                pass
        return options

    def search(self, query):
        """
        Get the available results from this searcher.

        .
        """
        query = query.replace(' ', '+')
        options = []
        # options += self._ff_options(query)
        options += self._sci_options(query)
        return options


def _truncate(s:str, n:int) -> str:
    """
    Truncate a string to a given length.

    Concat ellipses if truncated.
    """
    if len(s) <= n:
        return s

    return s[:n - 1] + "…"

def _pad(s:str, n:int, align='right') -> str:
    """
    Pad a string to a given length.

    Concat spaces or truncate.

    Arguments:
        s (str): The string to pad
        n (int): The length to pad to

    Returns:
        str: The padded string

    """
    ss = list(" " * n)
    t = _truncate(s, n)
    # for i, m in enumerate(t):
    #     ss[i] = m
    ss[0:len(t)] = t
    return "".join(ss)


DEFAULT_PREFERRED_TYPES = [
    'mobi', 'azw', 'txt'
]

DEFAULT_SEARCHERS = [
    # GutenbergSearcher,
    LibGenSearcher,
    ManyBooksSearcher,
]

BOOK_SEARCHERS = DEFAULT_SEARCHERS
ARTICLE_SEARCHERS = [
    # LibGenSearcher
]

def filenameize(name: str):
    return re.sub("\W+", "-", re.sub("['\"`]+", "", name.strip()))

class Booksnake:

    def __init__(self, preferred_types: List[str] = None):
        self.searchers = DEFAULT_SEARCHERS

        if preferred_types:
            self.preferred_types = preferred_types
        else:
            self.preferred_types = DEFAULT_PREFERRED_TYPES

    def search(self, query: str) -> List['Result']:
        """
        Search for books.

        .
        """
        results = []
        for s in self.searchers:
            results += s().search(query)
        results = sorted(results, key=lambda x: x.fmt not in self.preferred_types)
        return results

    def download(self, result: 'Result'):
        print(_attempt_url(result.url, result.fmt, filenameize(result.title)))


def print_results(
    results: List['Result'],
    color: bool = True,
    width: int = 80,
    preferred_types: List[str] = DEFAULT_PREFERRED_TYPES
):
    """
    Print results in a nice table.

    Arguments:

    Returns:

    """
    for i, result in enumerate(results):
        if color:
            print("{i}{indicator} {title} {author} {format} {source}".format(
                i=(
                    pretty_format([BLUE], "[{}]".format(_pad(str(i), 2)))
                ),
                indicator=(pretty_format([GREEN],
                    "*" if result.fmt in preferred_types else " "
                )),
                title=(pretty_format([BOLD, PURPLE, UNDERLINE],
                    _pad(result.title, int(max(10, width / 80 * 40)))
                )),
                author=(pretty_format([BOLD],
                    _pad(result.author, int(max(5, width / 80 * 20)))
                )),
                format=(pretty_format([BLUE],
                    _pad("[{}]".format(result.fmt), int(max(6, width / 80 * 7)))
                )),
                source=(pretty_format([],
                    _pad(result.source, int(max(4, width / 80 * 10)))
                ))
            ))
        else:
            print("{i}{indicator} {title} {author} {format} {source}".format(
                i="[{}]".format(_pad(str(i), 2)),
                indicator="*" if result.fmt in preferred_types else " ",
                title=_pad(result.title, int(max(10, width / 80 * 40))),
                author=_pad(result.author, int(max(5, width / 80 * 20))),
                format=_pad("[{}]".format(result.fmt), int(max(6, width / 80 * 7))),
                source=_pad(result.source, int(max(4, width / 80 * 10)))
            ))

def html_results(
    results: List['Result'],
    preferred_types: List[str] = DEFAULT_PREFERRED_TYPES
):
    """
    Print results in a nice table.

    Arguments:

    Returns:

    """
    return """
        <table>
            <thead>
                <th>Title</th>
                <th>Author</th>
                <th>Format</th>
                <th>Source</th>
            <thead>
            <tbody>{}</tbody>
        </table>""".format("".join(
        ["""
        <tr>
            <td>{title}</td>
            <td>{author}</td>
            <td>{format}</td>
            <td><a href='{url}'>{source}</a></td>
        </tr>
        """.format(
            title=result.title,
            author=result.author,
            format=result.fmt,
            url=result.url,
            source=result.source,
        ) for i, result in enumerate(results)]
    ))
