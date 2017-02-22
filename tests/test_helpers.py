# -*- coding: utf-8 -*-
# vim: foldmarker=[[[,]]]:foldmethod=marker

from __future__ import absolute_import, division, print_function

import datetime

from nose.tools import assert_equal, assert_not_equal, assert_raises_regexp, nottest  # NOQA
from freezegun import freeze_time

from hc.helpers import get_month_number, get_relative_month, get_date_from_relative_month


class Test():

    def test_get_month_number(self):
        assert_equal(1, get_month_number('Januar'))
        assert_equal(12, get_month_number('Dezember'))

    @freeze_time('2017-02-20')
    def test_get_relative_month(self):
        assert_equal(-2, get_relative_month(datetime.date(2016, 12, 1)))
        assert_equal(-1, get_relative_month(datetime.date(2017, 1, 1)))
        assert_equal(0, get_relative_month(datetime.date(2017, 2, 1)))
        assert_equal(0, get_relative_month(datetime.date.today()))
        assert_equal(0, get_relative_month(datetime.date(2017, 2, 28)))
        assert_equal(1, get_relative_month(datetime.date(2017, 3, 1)))
        assert_equal(10, get_relative_month(datetime.date(2017, 12, 1)))
        assert_equal(12, get_relative_month(datetime.date(2018, 2, 1)))

    @freeze_time('2017-02-20')
    def test_get_date_from_relative_month(self):
        assert_equal(datetime.date(2016, 12, 1), get_date_from_relative_month(-2))
        assert_equal(datetime.date(2017, 1, 1), get_date_from_relative_month(-1))
        assert_equal(datetime.date(2017, 2, 1), get_date_from_relative_month(0))
        assert_equal(datetime.date(2017, 3, 1), get_date_from_relative_month(1))
        assert_equal(datetime.date(2017, 12, 1), get_date_from_relative_month(10))
        assert_equal(datetime.date(2018, 2, 1), get_date_from_relative_month(12))
