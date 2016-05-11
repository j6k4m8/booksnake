#!/usr/bin/env python2
import sys
import os
import click
import libgenapi

import converter
import messenger
import downloader


def main(argv):
    if '-h' in argv:
        print """
        usage: booksnake [filename or url] [flags]

        Flags:
            -f      Specify a file format. Not needed if the file is local.
            -k      Keep files after processing and sending.

        Examples:
            booksnake ~/ebooks/HitchhikersGuide.mobi
                                        Sends the ebook; no conversion needed.

            booksnake ~/ebooks/HitchhikersGuide.epub
                                        First, converts the epub to mobi. Then,
                                        sends just as above.

            booksnake ~/ebooks/HitchhikersGuide.epub -k
                                        Converts and sends, but does not delete
                                        the temporary files after email is sent
                                        Note the -k (KEEP) flag.

            booksnake http://arthur.dent.com/HitchhikersGuide.html -f html
                                        Navigates to the URL (use quotes if the
                                        URL contains spaces) and downloads the
                                        file. You *must* specify a format using
                                        the -f flag; this is because some sites
                                        use a vanity URL (site.com/download/)
                                        and a format is not specified.
                                        (I'm working on fixing this...)

            NOTE: As of right now, flags cannot be combined (e.g. -fk fails).
        """
        return
    if len(argv) >= 1:
        if argv[0].startswith('http'):
            if '-f' in argv:
                _fmt = argv[argv.index('-f') + 1]
                filename = downloader.download_uri(argv[0], fmt=_fmt)
            else:
                print "No format given, try `-f mobi` or `-f html` or whatever"
                return
        elif argv[0].startswith('magnet:?'):
            # download all files to a temporary subdirectory,
            # then scan through, and all [pdf, html, epub] files should
            # be iteratively converted and emailed.
            print "Currently, magnet links are unsupported. Sorry! -jm"
            return
        else:
            filename = argv[0]
    else:
        return

    base_filename = '.'.join(filename.split('.')[:-1])

    # Convert if necessary
    if converter.get_file_extension(filename) == 'epub':
        converter.convert_epub(filename)
        final_filename = base_filename + '.mobi'
    if converter.get_file_extension(filename) == 'pdf':
        converter.convert_pdf(filename)
        final_filename = base_filename + '.mobi'
    else:
        final_filename = filename

    print final_filename

    if os.path.isfile(final_filename):
        if '--convert-only' in argv:
            print "Done: {}".format(final_filename)
        else:
            print "Sending..."
            messenger.send_file(final_filename)
    else:
        print "Conversion failed."

    if '-k' not in argv:
        os.system('rm ./.booksnake_*')

if __name__ == "__main__":
    main(sys.argv[1:])
