# booksnake

**[![CircleCI](https://circleci.com/gh/j6k4m8/booksnake.svg?style=svg)](https://circleci.com/gh/j6k4m8/booksnake)**

Booksnake is a tool to search the web for ebooks and automagically send them to your Kindle (or email), all as simply as possible.

> NOTE: Please only use booksnake for legal download of public-domain resources!

**Pull-requests and GitHub Issues are always welcome!**

## Installation

Spin up your favorite terminal, and boop this puppy right up in there:
```shell
pip install booksnake
```

Q.E.D. wut up

## Setup
This step is entirely optional, but if you don't want to have to specify `--to_email`, `--from_email`, and then type your email password every time you send, then you can add the following to a `~/.booksnakerc`:

```json
{
    "from_email": "you@gmail.com",
    "smtp_password": "your gmail password",
    "to_email": "you@free.kindle.com"
}
```

If you don't feel comfortable leaving your password in plaintext in your home directory (and I can't _possibly_ imagine why that would be!), you can omit that keyvalue pair and enter it at runtime.

You may also choose, like I did, to make a standalone gmail for just this purpose, and then the password is a moot point.

**Make sure that regardless of which email you use, you have added it to your [Authorized Senders](https://www.amazon.com/gp/help/customer/display.html?nodeId=201974240) in Amazon's Kindle settings, or else Amazon will refuse to send your documents to your device.**

## Usage

### Searching for, downloading, and sending a book

```shell
booksnake --query "Moby Dick"
```

[![asciicast](https://asciinema.org/a/esbwna82m297lbwhhvm2w95ne.png)](https://asciinema.org/a/esbwna82m297lbwhhvm2w95ne)

### Sending a book from a known URL
```shell
booksnake --url "http://mobydick.com/mobydick.mobi"
```

### Sending a book from a local file:
```shell
booksnake --file "~/books/mobydick.mobi"
```

## Advanced Usage

### Converting Files
If you're a _hacking wizard_ and you have Amazon's [`kindlegen`](https://www.amazon.com/gp/feature.html?docId=1000765211) installed, you may be able to convert some subset of epubs and pdfs to mobi, and send those to your kindle as well. As long as `kindlegen` is callable globally (e.g. you've put it in `/usr/bin` or somesuch), there's no difference in how you call booksnake:

```shell
booksnake --file "~/books/mobydick.epub"
```

### Preventing Sends, or Keeping Files
If you want to prevent booksnake from deleting the files after downloading and sending, you can pass the `--keep` flag:

```shell
booksnake --keep --query "Great Expectations"
```

You can combine this with `--no-send` if you want to _only_ download and convert the file, and not send it:

```shell
booksnake --keep --no-send --query "Great Expectations"
```
