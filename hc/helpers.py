# -*- coding: utf-8 -*-

"""
hc helpers
"""

from __future__ import absolute_import

import datetime
from dateutil.relativedelta import relativedelta


def get_month_number(month_name):
    return {
        'Januar': 1,
        'Februar': 2,
        'März': 3,
        'April': 4,
        'Mai': 5,
        'Juni': 6,
        'Juli': 7,
        'August': 8,
        'September': 9,
        'Oktober': 10,
        'November': 11,
        'Dezember': 12,
    }[month_name]


def get_relative_month(date):
    cur_date = datetime.date.today()
    return (date.year * 12 + date.month) - (cur_date.year * 12 + cur_date.month)


def get_date_from_relative_month(relative_month):
    cur_date = datetime.date.today()
    date = cur_date + relativedelta(months=relative_month)
    return datetime.date(date.year, date.month, 1)
