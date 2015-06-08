# booksnake
A command-line tool to download, convert, and send eBooks to your kindle from the web as simply as possible.

# Usage

----------------
Currently working:

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


-----------------
Not yet implemented:

- Remote File
    ```
    booksnake 'https://ebook-website.com/ebooks/HitchhikersGuide.mobi'
    ```
    Downloads the book and sends it to your Kindle. Use the `--keep` (`-k`) flag to retain the file after sending. Otherwise, it'll be deleted.


# Requirements

- Only tested on Ubuntu 14.04.
- Gmail account (do you know your password?)
- `kindlegen`, a cli epub-to-mobi converter from Amazon. (Download [here](http://www.amazon.com/gp/feature.html?docId=1000765211).) Must be globally callable, so I moved my executable to `/bin/`: `cd ~/Downloads/kindlegen /bin/`
- `aria2` will be used for downloading files in a future release.

# Setup
- Rename `demo-settings.py` to `settings.py`, and fill in your kindle email (I use `[username]@free.kindle.com` to avoid charges), your gmail username, and gmail password. Yeah, you're writing it out in plaintext, so... I guess be careful or whatever.
- Make booksnake executable, if it isn't already. `chmod +x ./booksnake`
- Run booksnake with the name of the file as its only argument: `./booksnake HitchhikersGuide.epub`
- Go read a book or something
