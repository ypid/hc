# -*- coding: utf-8 -*-

"""
Command line interface of hc
"""

from __future__ import absolute_import, division, print_function

import sys
import logging
import textwrap
import argparse
import pprint
import json
import datetime

from appdirs import user_cache_dir
from ruamel import yaml  # pylint: disable=import-error

from ._meta import __version__
from .yaml import dump_holidays_as_yaml
from .schulferien_org import SchulferienOrg
from .opening_hours_js import OpeningHoursJS

__all__ = ['main']

LOG = logging.getLogger(__name__)


def get_args_parser():
    args_parser = argparse.ArgumentParser(
        prog='hc',
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


def main():  # pylint: disable=too-many-branches
    args_parser = get_args_parser()
    args = args_parser.parse_args()
    if args.loglevel is None:
        args.loglevel = logging.WARNING
    logging.basicConfig(
        format='%(levelname)s{}: %(message)s'.format(
            ' (%(filename)s:%(lineno)s)' if args.loglevel <= logging.DEBUG else '',
        ),
        level=args.loglevel,
    )

    if args.input_format in ['schulferien_html']:
        if args.input_file:
            LOG.error("--input-file given but {} does not support this. Ignoring.".format(
                args.input_format,
            ))

    if args.update_output and args.output_file == '-':
        args_parser.error(
            "--update-output is not supported for STDIN/STDOUT."
        )

    defs = {}

    cache_dir = args.cache_dir
    if not cache_dir:
        cache_dir = user_cache_dir("hc")

    from_date = datetime.datetime.strptime(args.from_date, '%Y-%m').date()
    to_date = datetime.datetime.strptime(args.to_date, '%Y-%m').date()

    # Note that the class design is totally broken and should probably be redone.
    # ypid is aware of this.

    if args.update_output:
        with open(args.output_file, 'r', encoding='utf-8') as update_in_fh:
            if args.output_format == 'json':
                in_defs = json.load(update_in_fh)
            elif args.output_format == 'yaml':
                in_defs = yaml.load(update_in_fh, Loader=yaml.RoundTripLoader, preserve_quotes=True)

        if args.output_structure in 'opening_hours.js':
            opening_hours_js = OpeningHoursJS(
                defs=defs,
            )
            defs = opening_hours_js.read(in_defs)

        if LOG.isEnabledFor(logging.DEBUG):
            LOG.debug('defs after reading the to-be-updated file:\n{}'.format(
                pprint.pformat(defs),
            ))

    if args.input_format in 'schulferien_html':
        schulferien_org = SchulferienOrg(
            defs=defs,
            cache=args.cache,
            cache_dir=cache_dir,
        )
        defs = schulferien_org.get_school_holidays(from_date, to_date)

    if LOG.isEnabledFor(logging.DEBUG):
        LOG.debug('defs after performing update:\n{}'.format(
            pprint.pformat(defs),
        ))

    if args.output_structure in 'opening_hours.js':
        opening_hours_js = OpeningHoursJS(
            defs=defs,
        )
        out = opening_hours_js.get_school_holidays()

    if args.output_format == 'json':
        out_str = json.dumps(out, sort_keys=True, indent=2, ensure_ascii=False)
    elif args.output_format == 'yaml':
        out_str = dump_holidays_as_yaml(out)

    if LOG.isEnabledFor(logging.DEBUG):
        LOG.debug('output:\n{}'.format(out_str))

    if not args.dry_run:
        if args.output_file == '-':
            sys.stdout.write(out_str)
        else:
            with open(args.output_file, 'w', encoding='utf-8') as output_fh:
                output_fh.write(out_str)


if __name__ == '__main__':
    main()
