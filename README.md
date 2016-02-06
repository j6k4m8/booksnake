# booksnake
A command-line tool to download, convert, and send eBooks to your kindle from the web as simply as possible, in html, pdf, epub, or mobi formats.

# Usage

- Local Files
    ```
    booksnake ~/ebooks/HitchhikersGuide.mobi
    ```
    All this does is email the book using your gmail credentials.

- Convert Files
    ```
    booksnake ~/ebooks/HitchhikersGuide.epub
    ```
    Converts epub to mobi and sends it along. (Uses `kindlegen`)

- Remote File
    ```
    booksnake 'https://ebook-website.com/ebooks/HitchhikersGuide.mobi' -f mobi
    ```
    Downloads the book and sends it to your Kindle. Specify that you're downloading a mobi using the `-f` flag. Or download `-f html` or `-f epub`, I don't care. (This is because some links don't include the filename in them, or include a `?parameter` at the end, and booksnake is smart enough to follow links but it's not smart enough to always know the file you're downloading. So sue me.) Use the `--keep` (`-k`) flag to retain the file after sending. Otherwise, it'll be deleted.

-----------------
Not yet implemented:

- Magnet (Torrent) File
    ```
    booksnake 'magnet:?whatever-the-hell-magnet-links-look-like' -f mobi
    ```
    Planning on using aria2 for this. But... idk.


# Requirements

- Only tested on Ubuntu 14.04.
- Gmail account (do you know your password?)
- `kindlegen`, a cli epub-to-mobi converter from Amazon. (Download [here](http://www.amazon.com/gp/feature.html?docId=1000765211).) Must be globally callable, so I moved my executable to `/bin/`: `cp ~/Downloads/kindlegen /bin/`
- `aria2` will be used for downloading files in a future release.

# Setup
- Rename `demo-settings.py` to `settings.py`, and fill in your kindle email (I use `[username]@free.kindle.com` to avoid charges), your gmail username, and gmail password. Yeah, you're writing it out in plaintext, so... I guess be careful or whatever.
- Make booksnake executable, if it isn't already. `chmod +x ./booksnake`
- Run booksnake with the name of the file as its only argument: `./booksnake HitchhikersGuide.epub`
- Go read a book or something

# TODO

- Magnet links
- Intelligently guess what format has been downloaded (deprecate the `-f` flag)
- Ping the Goodreads API to add your brand new book to a specific shelf (`--goodreads-shelf "on-kindle"` or something)
