import urllib
import urllib.request
from bs4 import BeautifulSoup

# Uniformize "urlretrieve"
try:
    urlretrieve = urllib.urlretrieve
except:
    urlretrieve = urllib.request.urlretrieve


class BooksnakeSearcher:
    def __init__(self):
        self.base_url = ""

    def url(self, suffix=""):
        return "{}/{}".format(self.base_url, suffix)

    def get_options(self, query):
        pass


class LibreLibSearcher(BooksnakeSearcher):
    def __init__(self):
        self.base_url = "http://www.librelib.com"

    def get_options(self, query):
        query = query.replace(' ', '+')
        query = "/book?s=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        options = [[
            a.findAll('a')[0].text.strip(),     # author
            a.findAll('a')[1].text.strip(),     # title
            a.findAll('a')[-1].text.strip(),    # format
            a.findAll('a')[-1].get('href'),     # link
            a.findAll('td')[-2].text.strip()    # size
        ] for a in soup.findAll('tr')[1:]]
        return options


class LibgenSearcher(BooksnakeSearcher):
    def __init__(self):
        self.base_url = (
            "http://libgen.io" +
            "/foreignfiction/index.php?" +
            "s={}&f_lang=English&f_columns=0&f_ext=All"
        )

    def get_options(self, query):
        query = query.replace(' ', '+')
        f = urllib.request.FancyURLopener({}).open(self.base_url.format(query))
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        options = []
        for a in soup.findAll('table')[-1].findAll('tr'):
            link = a.findAll('a')[-1].get('href').replace(
                'ads.php', 'get.php'
            )
            if link[0] == "/":
                link = "http://libgen.io" + link
            options.append([
                a.findAll('td')[0].text.strip(),
                (
                    a.findAll('td')[1].text.strip() +
                    " " +
                    a.findAll('td')[2].text.strip()
                ),
                a.findAll('td')[-1].text.strip().split('(')[0],
                link,
                a.findAll('td')[-1].text.strip().split('(')[1][:-1]
            ])
        return options


class GutenbergSearcher(BooksnakeSearcher):
    def __init__(self):
        self.base_url = "https://www.gutenberg.org"

    def get_options(self, query):
        query = query.replace(' ', '+')
        query = "/ebooks/search/?query=" + query
        f = urllib.request.FancyURLopener({}).open(self.base_url + query)
        try:
            content = f.read()
        except:
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
