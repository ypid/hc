# -*- coding: utf-8 -*-

"""
Command line parser of hc
"""

from __future__ import absolute_import, division, print_function

import argparse
import textwrap
import datetime
import logging

from ._meta import __version__


def get_args_parser():
    args_parser = argparse.ArgumentParser(
        description=textwrap.dedent("""
            Holiday converter tool
        """),
        # epilog=__doc__,
    )
    args_parser.add_argument(
        '-V', '--version',
        action='version',
        version=__version__,
    )
    args_parser.add_argument(
        '-d', '--debug',
        help="Write debugging and higher to STDOUT|STDERR.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args_parser.add_argument(
        '-v', '--verbose',
        help="Write information and higher to STDOUT|STDERR.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    args_parser.add_argument(
        '-q', '--quiet', '--silent',
        help="Only write errors and higher to STDOUT|STDERR.",
        action="store_const",
        dest="loglevel",
        const=logging.ERROR,
    )
    args_parser.add_argument(
        '-n', '--no-cache',
        help="Do not cache intermediary files.",
        action="store_false",
        dest="cache",
    )
    args_parser.add_argument(
        '-c', '--cache-dir',
        help="Cache directory, defaults to the default cache directory of your operating system.",
    )
    args_parser.add_argument(
        '-i', '--input-file',
        help="File path to the input file to process."
        " '-' will read from STDIN.",
    )
    args_parser.add_argument(
        '-f', '--input-format', '--from',
        help="Format of the input file."
        " Default: %(default)s.",
        default='schulferien_html',
        choices=['schulferien_html'],
    )
    args_parser.add_argument(
        '-F', '--from-date',
        help="Process date range starting at given RFC 3339 date."
        " Default: Current year and month \"%(default)s\".",
        default=datetime.date.today().strftime('%Y-%m'),
    )
    args_parser.add_argument(
        '-T', '--to-date',
        help="Process date range ending at given RFC 3339 date."
        " Default: One year in the further \"%(default)s\".",
        default=(datetime.date.today() + datetime.timedelta(365)).strftime('%Y-%m'),
    )
    args_parser.add_argument(
        'output_file',
        help="Where to write the output file."
        " '-' will write to STDOUT.",
        metavar='output-file',
    )
    args_parser.add_argument(
        '-u', '--update-output',
        help="Update the output file instead of constructing it from scratch. Implementation incomplete.",
        action="store_true",
    )
    args_parser.add_argument(
        '-t', '--output-format', '--to',
        help="Format of the output file."
        " Default: %(default)s.",
        default='yaml',
        choices=['yaml', 'json'],
    )
    args_parser.add_argument(
        '-s', '--output-structure',
        help="Structure of the output file."
        " Default: %(default)s.",
        default='opening_hours.js',
        choices=['opening_hours.js'],
    )
    args_parser.add_argument(
        '-D', '--dry-run',
        help="Don't write output.",
        action="store_true",
    )

    return args_parser
