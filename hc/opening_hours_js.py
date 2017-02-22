# -*- coding: utf-8 -*-

"""
OpenStreetMap opening_hours.js format.
Refer to https://github.com/opening-hours/opening_hours.js/blob/master/holidays/README.md for the "spec".
"""

import logging
import pprint
from copy import deepcopy
from collections import OrderedDict

from .defaults import SH_ORDER

LOG = logging.getLogger(__name__)


def find_ind(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


class OpeningHoursJS(object):
    FIRST_LEVEL_SORTING = {
        # key -> weight
        '_nominatim_url': '10',
        'PH': '20',
        'SH': '30',
    }
    SH_DATA_SORTING = {
        # key -> weight
        'name': '0',
    }

    def __init__(self, defs=None):

        if defs is None:
            self._defs = {}
        else:
            self._defs = defs

    @staticmethod
    def update_sh_format(sh_data):
        if isinstance(sh_data, list):
            old_sh_data = deepcopy(sh_data)
            sh_data = {}
            for holiday_dict in old_sh_data:
                sh_data[holiday_dict['name']] = holiday_dict
                del sh_data[holiday_dict['name']]['name']

        return sh_data

    def read(self, in_defs):
        self._defs = in_defs

        for first_level in self._defs:
            if first_level == 'PH' or first_level.startswith('_'):
                continue
            elif first_level == 'SH':
                self._defs[first_level] = {}
                if '_nominatim_url' in in_defs[first_level]:
                    self._defs[first_level]['_nominatim_url'] = in_defs[first_level]['_nominatim_url']
                #  self._defs[first_level] = self.update_sh_format(self._defs[first_level])
            else:
                for second_level in self._defs[first_level]:
                    if second_level == 'SH':
                        self._defs[first_level][second_level] = {}
                        if '_nominatim_url' in in_defs[first_level][second_level]:
                            self._defs[first_level][second_level]['_nominatim_url'] = \
                                in_defs[first_level][second_level]['_nominatim_url']
                        #  self._defs[first_level][second_level] = self.update_sh_format(
                        #      self._defs[first_level][second_level]
                        #  )

        return self._defs

    def get_school_holidays(self, out=None):
        if out is None:
            out = OrderedDict()

        for region in sorted(self._defs, key=lambda k: self.FIRST_LEVEL_SORTING.get(k, k)):
            out.setdefault(region, OrderedDict())

            if region == 'PH' or region.startswith('_'):
                out[region] = self._defs[region]
                LOG.debug('Skipping: {}'.format(region))
                continue

            if LOG.isEnabledFor(logging.DEBUG):
                LOG.debug('Processing:\n{}'.format(
                    pprint.pformat(self._defs[region]),
                ))

            for second_level in self._defs[region]:
                if second_level == 'PH' or second_level.startswith('_'):
                    out[region][second_level] = self._defs[region][second_level]

            if 'SH' not in self._defs[region]:
                continue

            for holiday_name in SH_ORDER['de']:
                if holiday_name not in self._defs[region]['SH']:
                    #  LOG.debug('Not found {}, skipping'.format(holiday_name))
                    continue

                out[region].setdefault('SH', [])
                hol_def = self._defs[region]['SH'][holiday_name]

                ind = find_ind(out[region]['SH'], 'name', holiday_name)
                if ind == -1:
                    out[region]['SH'].append({
                        'name': holiday_name,
                    })
                    ind = find_ind(out[region]['SH'], 'name', holiday_name)
                out[region]['SH'][ind].update(hol_def)
                out[region]['SH'][ind] = OrderedDict(sorted(
                    out[region]['SH'][ind].items(),
                    key=lambda kv: self.SH_DATA_SORTING.get(kv[0], kv[0]),
                ))

        return out
