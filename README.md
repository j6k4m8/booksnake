# booksnake
A command-line tool to download, convert, and send eBooks to your kindle from the web as simply as possible, in html, pdf, epub, or mobi formats.

Pull requests and bug reports welcome!

# Requirements
- Only tested on Ubuntu 14.04 and OS X.
- Gmail account (do you know your password?)
- `smtplib`, `mimetypes`, `email`, `BeautifulSoup`, as per the `requirements.txt`

## Soft Requirements
- `kindlegen`, a cli epub-to-mobi converter from Amazon. (Download [here](http://www.amazon.com/gp/feature.html?docId=1000765211).) Must be globally callable, so I moved my executable to `/bin/`: `cp ~/Downloads/kindlegen /bin/`
- `aria2` will be used for downloading files in a future release.

# Setup

```
pip install booksnake
```

Or clone this repository and install the latest version from source:

```
git clone https://github.com/j6k4m8/booksnake.git
cd booksnake
pip install -U .
```

Now, create a `~/.booksnakerc` file (not necessary, but makes it so you don't have to specify `--from-email`, `--to-email`, and SMTP password every time). This is JSON:

```
{
    "from_email": "you@gmail.com",
    "smtp_password": "your gmail password",
    "to_email": "you@free.kindle.com"
}
```

If you don't feel comfortable putting any of these values in plaintext in your config file, then just omit that line. `--from-email` and `--to-email` can be specified when you call `booksnake`, and if you omit the SMTP password, booksnake will prompt you for it once it's time to send your file.

# Usage

- Search online (only for freely available, public-domain books):
    ```
    booksnake --query "My Title"
    ```

- Download a book from a URL:
    ```
    booksnake --url "http://my.books.com/title.mobi"
    ```

- Send a local file:
    ```
    booksnake --file "title.mobi"
    ```

## Help Message
```
usage: booksnake [-h] [--from FROM_EMAIL] [--to TO_EMAIL] [--gutenberg]
                 [--no-gutenberg] [--keep] [--no-keep] [--send] [--no-send]
                 (--query QUERY | --file FILENAME | --url URL | --magnet MAGNET)

Search and send books to Kindle.

optional arguments:
  -h, --help            show this help message and exit
  --from FROM_EMAIL     An authorized sender on your Amazon account.
  --to TO_EMAIL         Your Kindle's email address (foo@free.kindle.com)
  --gutenberg           Explicitly use Gutenberg as a search engine
  --no-gutenberg        Explicitly DON'T use Gutenberg as a search engine
  --keep                Keep the file(s) when booksnake exits
  --no-keep             [Default] Delete the file(s) when booksnake exits
  --send                [Default] Send the file when done processing
  --no-send             Do not send the file when done processing. (Use with
                        --keep)
  --query QUERY, -q QUERY
                        If you're searching for a file, the search terms.
  --file FILENAME, -f FILENAME
                        If you're sending a downloaded file, the filename.
  --url URL, -u URL     If you're sending a downloadable file, the URL.
  --magnet MAGNET, -m MAGNET
                        If you're downloading via a magnet link
```

# TODO

- Magnet links
- Intelligently guess what format has been downloaded (deprecate the `-f` flag)
- Ping the Goodreads API to add your brand new book to a specific shelf (`--goodreads-shelf "on-kindle"` or something)
