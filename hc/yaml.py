# -*- coding: utf-8 -*-

"""
YAML representation
"""

# pylint: disable=no-member

from __future__ import absolute_import

import io
import re
from collections import OrderedDict

from ruamel import yaml  # pylint: disable=import-error
import pyaml

from .datatypes import PhData, MonthDayList


class PrettyHolidayYAMLDumper(yaml.RoundTripDumper):  # pylint: disable=too-many-ancestors
    """YAML dumper optimized human readability of the holiday format."""

    def represent_dict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data, flow_style=False)

    def represent_list(self, data):
        return self.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


PrettyHolidayYAMLDumper.add_representer(dict, PrettyHolidayYAMLDumper.represent_dict)
PrettyHolidayYAMLDumper.add_representer(OrderedDict, PrettyHolidayYAMLDumper.represent_dict)
PrettyHolidayYAMLDumper.add_representer(MonthDayList, PrettyHolidayYAMLDumper.represent_list)
PrettyHolidayYAMLDumper.add_representer(PhData, PrettyHolidayYAMLDumper.represent_list)


def get_clean_yaml(serialized_data, add_vspacing=False):
    serialized_buf = io.BytesIO(serialized_data.encode("utf-8"))
    if add_vspacing:
        pyaml.dump_add_vspacing(serialized_buf, [1])

    # Workaround: https://bitbucket.org/ruamel/yaml/issues/66/indentation-issue
    serialized_buf.seek(0)
    result = list()
    for line in serialized_buf:
        line = line.decode('utf-8')
        line = re.sub(r'^(\s\s[-\s]\s|-\s)', r'  \1', line)
        # https://gitlab.com/ypid/hc/builds/11250795
        # Not sure why but one of the dependency updates might have
        # broken/introduced trailing whitespace?!
        line = re.sub(r' +$', '', line)
        result.append(line)
    serialized_buf.seek(0)
    serialized_buf.truncate()
    serialized_buf.write(''.join(result).encode('utf-8'))

    return serialized_buf.getvalue().decode('utf-8')


def dump_holidays_as_yaml(unserialized_data, add_vspacing=True):
    serialized_data = yaml.dump(
        unserialized_data,
        Dumper=PrettyHolidayYAMLDumper,
        allow_unicode=True,
        width=120,
        explicit_start=True,
        #  block_seq_indent=2,
        #  indent=4,
    )

    return get_clean_yaml(serialized_data, add_vspacing=add_vspacing)
