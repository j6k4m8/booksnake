import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import requests

# Uniformize "urlretrieve"
try:
    urlretrieve = urllib.urlretrieve
except Exception as exc:
    urlretrieve = urllib.request.urlretrieve


class BooksnakeOption(object):
    def __init__(self, url, size, fmt, title, author, source="Unknown"):
        self.url = url
        self.size = size
        self.fmt = fmt
        self.title = title
        self.author = author
        self.source = source


class BooksnakeSearcher(object):
    """
    The abstract searcher class for remote query lookup.
    Not useful to you!

    """
    def __init__(self):
        self.base_url = ""

    def url(self, suffix=""):
        """
        Generate a URL for this searcher
        """
        return "{}/{}".format(self.base_url, suffix)

    def get_options(self, query):
        """
        Return options based on a query, using this searcher
        """
        pass


class LibreLibSearcher(BooksnakeSearcher):
    """
    Search www.librelib.com.

    Appears to be defunct.
    """
    def __init__(self):
        self.base_url = "http://www.librelib.com"

    def get_options(self, query):
        query = query.replace(' ', '+')
        query = "/book?s=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        options = [BooksnakeOption(
            author=a.findAll('a')[0].text.strip(),     # author
            title=a.findAll('a')[1].text.strip(),      # title
            fmt=a.findAll('a')[-1].text.strip(),       # format
            url=a.findAll('a')[-1].get('href'),        # link
            size=a.findAll('td')[-2].text.strip(),     # size
            source="LibreLib"
        ) for a in soup.findAll('tr')[1:]]
        return options


class ManyBooksSearcher(BooksnakeSearcher):
    """
    Searches www.manybooks.net
    """
    def __init__(self):
        self.base_url = "http://www.manybooks.net"

    def get_options(self, query):
        query = query.replace(' ', '+')
        query = "/search.php?search=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        entries = soup.find_all('div', class_=["row", "grid_12"])
        options = [BooksnakeOption(
            author=re.findall("<br/>by (.*)", str(a))[0],
            title=a.find_all("a")[0].text,
            fmt="azw",
            url="{}/send/1:kindle:.azw:kindle/{}/{}.azw".format(
                self.base_url, *[
                    a.find_all('a')[0].attrs['href']
                    .replace(".html", "")
                    .replace("/titles/", "")
                ] * 2),
            size="?",
            source="ManyBooks"
        ) for a in entries]
        return options


class LibgenSearcher(BooksnakeSearcher):
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
                    ".*\((.*)\).*",
                    a.findAll('td')[-1].text.strip()
                )[0]
            except Exception as exc:
                pass
            options.append(BooksnakeOption(
                url=link,
                size=size,
                fmt=a.findAll('td')[-1].text.strip().split('(')[0],
                title=(
                    a.findAll('td')[1].text.strip() +
                    " " +
                    a.findAll('td')[2].text.strip()
                ),
                author=a.findAll('td')[0].text.strip(),
                source="Libgen"
            ))
        return options

    def _sci_options(self, query):
        content = requests.get(self.sci_base_url.format(query)).text
        soup = BeautifulSoup(content, 'html.parser')
        options = []
        for a in soup.findAll('table')[2].findAll('tr')[1:]:
            link = [
                ll for ll in a.findAll('a')
                if 'ads.php' in ll.get('href', '')
            ][0].get('href').replace(
                'ads.php', 'get.php'
            )

            if link[0] == "/":
                link = "http://libgen.io" + link

            size = "   "
            try:
                size = re.findall(
                    ".*\((.*)\).*",
                    a.findAll('td')[-1].text.strip()
                )[0]
            except Exception as exc:
                pass
            options.append(BooksnakeOption(
                url=link,
                size=a.findAll('td')[7].text.strip(),
                fmt=a.findAll('td')[8].text.strip(),
                title=(
                    a.findAll('td')[2].text.strip()
                ),
                author=a.findAll('td')[1].text.strip(),
                source="Libgen"
            ))
        return options

    def get_options(self, query):
        query = query.replace(' ', '+')
        options = []
        # options += self._ff_options(query)
        options += self._sci_options(query)
        return options


class GutenbergSearcher(BooksnakeSearcher):
    """
    Searches Project Gutenberg
    """
    def __init__(self):
        self.base_url = "https://www.gutenberg.org"

    def get_options(self, query):
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
                "and have been banned for 24 hours by their rate-limiter. " +
                "The --no-gutenberg flag has been added to ~/.booksnakerc " +
                "to prevent this from happening. Use the --gutenberg flag " +
                "to explicitly enable this for a query."
            )
            settings['searchers.gutenberg'] = False
            save_settings()
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

            options.append([
                author,                         # author
                title,                          # title
                'mobi',                         # format (cheating)
                self.url(
                    a.find('a').get('href') +
                    ".kindle.images"
                ),                              # link
                ' ',                            # size unlisted
            ])
        return options
