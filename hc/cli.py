# -*- coding: utf-8 -*-

"""
Command line interface of hc
"""

from __future__ import absolute_import, division, print_function

import sys
import logging
import pprint
import json
import datetime

from appdirs import user_cache_dir
from ruamel import yaml

from .cli_parser import get_args_parser
from .yaml import dump_holidays_as_yaml
from .schulferien_org import SchulferienOrg
from .opening_hours_js import OpeningHoursJS

__all__ = ['main']

LOG = logging.getLogger(__name__)


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
