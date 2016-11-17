# booksnake
A command-line tool to download, convert, and send eBooks to your kindle from the web as simply as possible, in html, pdf, epub, or mobi formats.

Pull requests and bug reports welcome!

# Requirements

- Only tested on Ubuntu 14.04 and OS X.
- Gmail account (do you know your password?)
- `kindlegen`, a cli epub-to-mobi converter from Amazon. (Download [here](http://www.amazon.com/gp/feature.html?docId=1000765211).) Must be globally callable, so I moved my executable to `/bin/`: `cp ~/Downloads/kindlegen /bin/`
- `aria2` will be used for downloading files in a future release.
- `smtplib`, `mimetypes`, `email`, `BeautifulSoup`, `libgenapi`. pip install them all!

# Setup

First, create a `~/.booksnakerc` file (not necessary, but makes it so you don't have to specify `--from-email`, `--to-email`, and SMTP password every time). This is JSON:

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
    [![asciicast](https://asciinema.org/a/2ji7kxe7840xqiyujxtjyrkkg.png)](https://asciinema.org/a/2ji7kxe7840xqiyujxtjyrkkg)

- Download a book from a URL:
    ```
    booksnake --url "http://my.books.com/title.mobi"
    ```

- Send a local file:
    ```
    booksnake --file "title.mobi"
    ```

# TODO

- Magnet links
- Intelligently guess what format has been downloaded (deprecate the `-f` flag)
- Ping the Goodreads API to add your brand new book to a specific shelf (`--goodreads-shelf "on-kindle"` or something)
