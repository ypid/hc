# -*- coding: utf-8 -*-

"""
schulferien.org interface
"""

# Potential alternative sources:
#
# * http://www.schulferien.org/Schulferien_nach_Jahren/2016/schulferien_2016.html

# pylint: disable=too-many-locals,too-many-nested-blocks,too-many-branches

import os
import re
import tempfile
import logging
import datetime
from dateutil.rrule import rrule, MONTHLY

from pyquery import PyQuery as pq
import xmltodict
import requests
import requests_cache

from .defaults import SH_ORDER
from .helpers import get_month_number, get_relative_month
from .datatypes import MonthDayList

__all__ = ['SchulferienOrg']

LOG = logging.getLogger(__name__)


class SchulferienOrg(object):

    _SCHOOL_HOLIDAYS_HTML_URL = 'http://www.schulferien.org'

    def __init__(self, defs=None, cache=True, cache_dir=None):

        if defs is None:
            self._defs = {}
        else:
            self._defs = defs

        self._cache = cache
        self._cache_dir = cache_dir

        if self._cache:
            if not self._cache_dir:
                self._cache_dir = os.path.join(tempfile.gettempdir(), 'hc')
            os.makedirs(self._cache_dir, exist_ok=True)  # pylint: disable=unexpected-keyword-arg

            requests_cache.install_cache(os.path.join(self._cache_dir, 'requests_cache'))

    def get_month_dataset(self, date):
        cache_dir = os.path.join(self._cache_dir, 'www.schulferien.org', 'de', 'SH', str(date.year))
        cache_file = os.path.join(cache_dir, '{}.html'.format(date.month))

        if self._cache and os.path.isfile(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as cache_fh:
                month_dataset = cache_fh.read()
        else:
            url = "{}/?action=mt&controller=kalender&m={}".format(
                self._SCHOOL_HOLIDAYS_HTML_URL,
                get_relative_month(date),
            )
            # Don’t cache those URL requests because the request parameters are not
            # deterministic as they are relative to the current year and month.
            with requests_cache.disabled():
                month_dataset = requests.get(url).text

            if self._cache:
                os.makedirs(cache_dir, exist_ok=True)  # pylint: disable=unexpected-keyword-arg
                with open(cache_file, 'w', encoding='utf-8') as cache_fh:
                    cache_fh.write(month_dataset)

        return month_dataset

    def _fix_upstream_mistakes(self):
        """
        Nobody is perfect. Some mistakes have being found in schulferien.org
        data which is patched here until it has been fixed upstream.
        The thing which makes ypid a bit scared is that the mistakes where not
        present in the ical files which are supposed to be generated from the
        same source as the html files. Wired.
        """

        if 'Baden-Württemberg' in self._defs:
            if 'SH' in self._defs['Baden-Württemberg']:
                if 'Herbstferien' in self._defs['Baden-Württemberg']['SH']:
                    if '2014' in self._defs['Baden-Württemberg']['SH']['Herbstferien']:
                        self._defs['Baden-Württemberg']['SH']['Herbstferien']['2014'] = MonthDayList([10, 27, 10, 30])

    def get_school_holidays(self, from_date, to_date):
        #  index_pq = pq(requests.get(self._SCHOOL_HOLIDAYS_HTML_URL).text)
        #  html_heading_table = index_pq("div.appointment_grid_table_container tbody").find("a span")
        #  regions = [e.text() for e in html_heading_table.items()]
        #  LOG.debug("Found regions: {}".format(regions))

        # Hard coded for now to not request the same resource multiple times during CI testing.
        regions = [
            'Baden-Württemberg', 'Bayern', 'Berlin', 'Brandenburg',
            'Bremen', 'Hamburg', 'Hessen', 'Mecklenburg-Vorpommern',
            'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz',
            'Saarland', 'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein',
            'Thüringen']
        LOG.debug("Hard coded regions: {}".format(regions))

        for region in regions:
            self._defs.setdefault(region, {})

        # The SH definitions start around 1952-04, great job!
        for date in rrule(MONTHLY, dtstart=from_date, until=to_date):
            month_dataset = self.get_month_dataset(date)
            month_pq = pq(month_dataset)

            month_name, year = month_pq("thead tr th.appointment_grid_monat_title").text().split(' ')
            year = int(year)
            month = get_month_number(month_name)
            year_month = "{}-{:0>2}".format(year, month)

            month_data = xmltodict.parse(month_pq("tbody").outerHtml())  # pylint: disable=no-member
            if not month_data['tbody'] or 'tr' not in month_data['tbody']:
                LOG.debug("No data available for {}, skipping.".format(
                    year_month,
                ))
                continue

            if len(month_data['tbody']['tr']) != len(regions):
                LOG.warning(
                    "There are {} regions defined"
                    " but the month dataset {} only provides data for {} regions."
                    " You might have to invalided the cache by deleting {}.".format(
                        len(regions),
                        len(month_data['tbody']['tr']),
                        year_month,
                        self._cache_dir,
                    )
                )

            sh_order = SH_ORDER['de']
            for ind, region_data in enumerate(month_data['tbody']['tr']):
                region = regions[ind]
                #  if region != 'Bayern':
                #      continue

                LOG.debug("Processing {}, {}".format(region, year_month))
                for day, data in enumerate(region_data['td'], 1):
                    classes = re.split(r'\s+', data['@class'].strip())
                    if 'ferien' in classes:
                        holiday_name = pq(data['@data-tip-text'])("b")[0].text.split(' ')[0]
                        self._defs[region].setdefault('SH', {})
                        self._defs[region]['SH'].setdefault(holiday_name, {})
                        hol_def = self._defs[region]['SH'][holiday_name]

                        day_before = datetime.date(year, month, day) - datetime.timedelta(1)

                        # Expect only the last holiday to wrap into the next year.
                        if sh_order.index(holiday_name) == len(sh_order)-1:
                            if (str(year-1) in hol_def and hol_def[str(year-1)][-2] ==
                                    day_before.month and hol_def[str(year-1)][-1] ==
                                    day_before.day):
                                hol_def[str(year-1)][-2] = month
                                hol_def[str(year-1)][-1] = day
                                continue

                        if str(year) in hol_def:
                            if hol_def[str(year)][-2] == day_before.month and hol_def[str(year)][-1] == day_before.day:
                                hol_def[str(year)][-2] = month
                                hol_def[str(year)][-1] = day
                            else:
                                hol_def[str(year)].extend([month, day, month, day])
                        else:
                            hol_def[str(year)] = MonthDayList([month, day, month, day])

        self._fix_upstream_mistakes()
        return self._defs
