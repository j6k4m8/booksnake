#!/usr/bin/env python3
from __future__ import absolute_import
import os
import sys
import json
import time
import argparse

from booksnake.printing import *
from booksnake.searchers import *
from booksnake.sending import *

# Uniformize 'input()'
try:
    input = raw_input
except NameError:
    pass

settings = {}
cleanups = []


def read_settings():
    """
    Read in the settings from a ~/.booksnakerc. If the file does not exist,
    then generate a new file.
    """
    global settings
    try:
        with open(os.path.expanduser('~/.booksnakerc'), 'r') as setfh:
            settings = json.load(setfh)
    except:
        pretty_print([YELLOW], "No ~/.booksnakerc file found, creating...")
        settings = {}
        save_settings()


def save_settings():
    """
    Write settings to ~/.booksnakerc.
    """
    with open(os.path.expanduser('~/.booksnakerc'), 'w+') as setfh:
        json.dump(
            settings, setfh, sort_keys=True, indent=4, ensure_ascii=False
        )


def convert_file(filename, ext):
    os.system('kindlegen "{}"'.format(filename))
    cleanups.append(filename)
    filename = ".".join(filename.split('.')[:-1]) + ".mobi"
    cleanups.append(filename)
    return filename


def process_file(filename):
    """
    Process a file.
    """
    filename = os.path.expanduser(filename)
    if not os.path.exists(filename):
        raise ValueError("No such file {}.".format(filename))

    ext = filename.split('.')[-1]
    if ext != 'mobi':
        # We need to convert.
        filename = convert_file(filename, ext)
    return filename


def _attempt_url(url, fmt="mobi", fname=None):
    """
    Attempts to download a file. Returns `None` if the download fails.
    """
    if fname is None:
        filename = ".booksnake_{}.{}".format(str(int(time.time())), fmt)
    else:
        filename = "{}.{}".format(fname, fmt)
    filename, _ = urlretrieve(url, filename)
    return filename


def process_url(url):
    """
    Process a url.
    """
    return _attempt_url(url)


def process_magnet(magnet):
    """
    Process a magnet.
    """
    pass


def _trunc(s, length):
    if len(s) > length:
        return s[:length - 3] + "..."
    else:
        return (s + (" " * length))[:length]
    return s


LIBRELIB = 1
GUTENBERG = 2


def cli_chooser(options):
    select_i = 1
    for pub in options:
        # Print number, format indicator*, author,
        # title, and format for each item.
        print("[{}]{}\t{}\t{}\t{}".format(
            select_i,
            [" ", "*"][pub[2] == 'mobi'],
            _trunc(pub[0], 20),
            pretty_format([GREEN], _trunc(pub[1], 40)),
            pretty_format([PURPLE], _trunc(pub[4], 7) + " " + pub[2])
        ))
        select_i += 1
    selection = input(
        "Select the book to download (1..{}): ".format(select_i - 1)
    )
    return selection


def always_choose_the_first_mobi_chooser(options):
    select_i = 1
    for pub in options:
        if pub[2] == 'mobi':
            return select_i
        select_i += 1


def process_query(query, modes=[], chooser=cli_chooser):
    """
    Process a query.
    """
    if type(modes) is not list:
        modes = [modes]

    if len(modes) is 0:
        modes = [GutenbergSearcher(), LibreLibSearcher(), LibgenSearcher()]

    options = []
    for s in modes:
        options += s.get_options(query)

    selection = chooser(options)
    choice = options[int(selection) - 1]
    return _attempt_url(
        choice[3].replace('download', 'get'), choice[2], choice[1]
    )


def delete_files():
    for fn in cleanups:
        try:
            os.remove(fn)
        except:
            pass


if __name__ == "__main__":
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

    parser.add_argument('--keep', dest='keep_file', action='store_true',
        help="Keep the file(s) when booksnake exits"
    )
    parser.add_argument('--no-keep', dest='keep_file', action='store_false',
        help="[Default] Delete the file(s) when booksnake exits"
    )
    parser.set_defaults(keep_file=False)

    parser.add_argument('--send', dest='send_file', action='store_true',
        help="[Default] Send the file when done processing"
    )
    parser.add_argument('--no-send', dest='send_file', action='store_false',
        help="Do not send the file when done processing. (Use with --keep)"
    )
    parser.set_defaults(send_file=True)

    source_group = parser.add_mutually_exclusive_group(required=True)
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

    if args.filename is not None:
        filename = args.filename
    elif args.url is not None:
        filename = process_url(args.url)
    elif args.magnet is not None:
        filename = process_magnet(args.magnet)
    else:
        # search if all else fails.
        searchers = []
        if sum([args.use_gutenberg, settings.get('searchers.gutenberg', False)]):
            searchers.append(GutenbergSearcher())
        searchers.append(LibreLibSearcher())
        searchers.append(LibgenSearcher())
        filename = process_query(args.query, modes=searchers)

    # Perform conversion, if necessary.
    filename = process_file(filename)
    # `filename` holds the name of the file to send.

    if args.send_file:
        cleanups += send_file(filename, args.from_email, args.to_email,
                              settings=settings)

    if not args.keep_file:
        delete_files()

    save_settings()
