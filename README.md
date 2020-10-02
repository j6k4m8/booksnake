# booksnake

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

Create a `~/.config/booksnake.json` file with the following contents:

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

No matter which command (`send`, `download`, or `search`) you use, Booksnake will show the same search results:

```shell
booksnake send connecticut yankee
1:	<Book "A Connecticut Yankee In King Arthur's Court" by Twain, Mark>
2:	<Book "A Connecticut Yankee in King Arthur's Court" by Twain, Mark>
3:	<Book "A Connecticut Yankee in King Arthur's Court" by Twain, Mark>
4:	<Book "Connecticut Yankee in King Arthur's Court, A" by Twain, Mark>
>
```

You are prompted to enter the ID number of the book you want to process. Enter an integer, and then hit Enter.

### Search for a book without downloading

```shell
booksnake search "Moby Dick"
```

### Download a book without sending

```shell
booksnake download "Moby Dick"
```

### Search for, download, and send a book to Kindle:

```shell
booksnake send "Moby Dick"
```
