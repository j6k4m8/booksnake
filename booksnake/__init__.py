#!/usr/bin/env python3

"""
The main driver for booksnake.

Download some delicious reads!
"""


from __future__ import absolute_import
import os
import sys
import json
import time
import argparse

from booksnake.printing import *
from booksnake.searchers import *
from booksnake.sending import *


__version__ = "0.2.2"

SETTINGS = {}
CLEANUPS = []
HANDLED_FILETYPES = ['mobi', 'html', 'azw']


def read_settings():
    """
    Read in the settings from a ~/.booksnakerc.

    If the file does not exist, then generate a new file.

    Arguments:
        None

    Returns:
        None

    """
    global SETTINGS
    try:
        # Open the settings file
        with open(os.path.expanduser('~/.booksnakerc'), 'r') as setfh:
            SETTINGS = json.load(setfh)
    except Exception as exc:
        # Indicate that a reconcilable failure occurred:
        pretty_print([YELLOW], "No ~/.booksnakerc file found, creating...")
        SETTINGS = {}
        save_settings()


def save_settings():
    """
    Write settings to ~/.booksnakerc.

    Arguments:
        None

    Returns:
        None

    """
    with open(os.path.expanduser('~/.booksnakerc'), 'w+') as setfh:
        # Write the settings to disk:
        json.dump(
            SETTINGS, setfh, sort_keys=True, indent=4, ensure_ascii=False
        )


def convert_file(filename):
    """
    Convert a file, using kindlegen.

    TODO: Possibly to utilize fallback converters such as pandoc?

    Arguments:
        filename (str): The path to the file on disk

    Returns:
        str: The new filename, after conversion

    """
    # Call the kindlegen executable.
    os.system('kindlegen "{}"'.format(filename))

    # Add the current filename to the list of things to delete:
    CLEANUPS.append(filename)

    # "Guess" the name that the converted file will have:
    filename = ".".join(filename.split('.')[:-1]) + ".mobi"
    CLEANUPS.append(filename)
    return filename


def process_file(filename):
    """
    Process a file.

    Arguments:
        filename (str): The path to the file on disk

    Returns:
        str: The filename of the processed file

    """
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        raise ValueError("No such file {}.".format(filename))

    ext = filename.split('.')[-1]
    if ext not in HANDLED_FILETYPES:
        # We need to convert.
        filename = convert_file(filename)
    return filename


def _attempt_url(url, fmt="mobi", fname=None):
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
    filename, _ = urlretrieve(url, filename)
    return filename


def process_url(url):
    """
    Process a url.

    Arguments:
        url (str): The HTTP url to attempt

    Returns:
        str: The filename as downloaded by _attempt_url

    """
    return _attempt_url(url)


def process_magnet(magnet):
    """
    Process a magnet.

    Arguments:
        magnet (str): The magnet link url

    Returns:
        str: The filename, as downloaded by the magnet downloader

    """
    raise NotImplementedError


def _trunc(truncatable, length):
    """
    Truncate a string s to length, including "...".

    Truncation helper-function to truncate string s at length=length.
    If len(s) < length, returns s with space-padding. If len(s) > length,
    return s, ending with ellipses (...), total-length = length.

    Arguments:
        s (str): The string to truncate
        length (int): The length at which to truncate

    Returns:
        str: Truncated string

    """
    if len(truncatable) > length:
        return truncatable[:length - 3] + "..."
    else:
        return (truncatable + (" " * length))[:length]
    return truncatable


LIBRELIB = 1
GUTENBERG = 2


def cli_chooser(options):
    """
    Use the CLI to let the user pick desired option.

    Arguments:
        options (str[][]): A list of options to provide

    Returns:
        Index into `options` to choose

    """
    select_i = 1
    for pub in options:
        # Print number, format indicator*, author,
        # title, size, and format for each item.
        print("[{}]{}\t{}\t{}\t{}".format(
            select_i,
            [" ", "*"][pub.fmt == 'mobi'],
            _trunc(pub.author, 20),
            pretty_format([GREEN], _trunc(pub.title, 40)),
            pretty_format([PURPLE], _trunc(pub.size, 7) + " " + pub.fmt + "\t(" + pub.source + ")")
        ))
        select_i += 1
    selection = input(
        "Select the book to download (1..{}): ".format(select_i - 1)
    )
    return selection


def always_choose_the_first_mobi_chooser(options):
    """
    A chooser that just picks the first mobi that it sees. Promiscuous!

    Arguments:
        options (str[][]): A list of options to provide

    Returns:
        Index into `options`
    """
    select_i = 1
    for pub in options:
        if pub.fmt == 'mobi':
            return select_i
        select_i += 1


def process_query(query, modes=[], chooser=cli_chooser):
    """
    Process a search query.

    Arguments:
        query (str): The query to search for. Needn't be escaped!
        modes (booksnake.searcher.BooksnakeSearcher[] : []): The searchers to
            use when looking up the query. If none are specified, all are used
        chooser (fn : cli_chooser): Which chooser to use when selecting. Uses
            the CLI when none is specified.

    Returns:
        str: filename of the downloaded file

    """
    if type(modes) is not list:
        modes = [modes]

    if len(modes) is 0:
        modes = [GutenbergSearcher(), LibreLibSearcher(), LibgenSearcher()]

    options = []
    for s in modes:
        try:
            # This fails in cases where the website is down or the HTML has
            # changed dramatically:
            options += s.get_options(query)
        except Exception as exc:
            # Should probably print out here or something...
            pretty_print([BOLD, YELLOW], "Failed to fetch from {} with error:".format(str(s)))
            pretty_print([YELLOW], str(exc))

    selection = chooser(options)
    choice = options[int(selection) - 1]
    return _attempt_url(
        choice.url, choice.fmt, choice.title
    )


def delete_files():
    """
    Remove all of the files in the `cleanup` array.

    If a deletion fails, does not notify the user.
    """
    for fname in CLEANUPS:
        try:
            os.remove(fname)
        except OSError as exp:
            pass


def main():
    """
    CLI main fn.

    Args:
        None
    """
    global CLEANUPS
    read_settings()
    parser = argparse.ArgumentParser(
        description='Search and send books to Kindle.'
    )
    parser.add_argument(
        '--from', dest='from_email', required=False, default=None,
        help='An authorized sender on your Amazon account.'
    )
    parser.add_argument(
        '--to', dest='to_email', required=False, default=None,
        help="Your Kindle's email address (foo@free.kindle.com)"
    )

    parser.add_argument(
        '--gutenberg', dest='use_gutenberg', action='store_true',
        help="Explicitly use Gutenberg as a search engine"
    )
    parser.add_argument(
        '--no-gutenberg', dest='use_gutenberg', action='store_false',
        help="Explicitly DON'T use Gutenberg as a search engine"
    )
    parser.set_defaults(use_gutenberg=False)

    parser.add_argument(
        '--keep', dest='keep_file', action='store_true',
        help="Keep the file(s) when booksnake exits"
    )
    parser.add_argument(
        '--no-keep', dest='keep_file', action='store_false',
        help="[Default] Delete the file(s) when booksnake exits"
    )
    parser.set_defaults(keep_file=False)

    parser.add_argument(
        '--send', dest='send_file', action='store_true',
        help="[Default] Send the file when done processing"
    )
    parser.add_argument(
        '--no-send', dest='send_file', action='store_false',
        help="Do not send the file when done processing. (Use with --keep)"
    )
    parser.set_defaults(send_file=True)

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument(
        '--version', '-v', dest='version', required=False, default=False,
        action='store_true',
        help="Get the version of the booksnake library running here."
    )
    source_group.add_argument(
        '--query', '-q', dest='query', required=False, default=None,
        help="If you're searching for a file, the search terms."
    )
    source_group.add_argument(
        '--file', '-f', dest='filename', required=False, default=None,
        help="If you're sending a downloaded file, the filename."
    )
    source_group.add_argument(
        '--url', '-u', dest='url', required=False, default=None,
        help="If you're sending a downloadable file, the URL."
    )
    source_group.add_argument(
        '--magnet', '-m', dest='magnet', required=False, default=None,
        help="If you're downloading via a magnet link"
    )
    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit()

    if args.filename is not None:
        filename = args.filename
    elif args.url is not None:
        filename = process_url(args.url)
    elif args.magnet is not None:
        filename = process_magnet(args.magnet)
    else:
        # search if all else fails.
        searchers = []
        if sum([
            args.use_gutenberg,
            SETTINGS.get('searchers.gutenberg', False)
        ]):
            searchers.append(GutenbergSearcher())
        searchers.append(LibreLibSearcher())
        searchers.append(ManyBooksSearcher())
        searchers.append(LibgenSearcher())
        filename = process_query(args.query, modes=searchers)

    # Perform conversion, if necessary.
    filename = process_file(filename)
    # `filename` holds the name of the file to send.

    if args.send_file:
        CLEANUPS += send_file(filename, args.from_email, args.to_email,
                              settings=SETTINGS)

    if not args.keep_file:
        delete_files()

    save_settings()


if __name__ == "__main__":
    main()
