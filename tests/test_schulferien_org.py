# -*- coding: utf-8 -*-
# vim: foldmarker=[[[,]]]:foldmethod=marker

from __future__ import absolute_import, division, print_function

import logging

from nose.tools import assert_equal, assert_not_equal, assert_raises_regexp, nottest  # NOQA

from hc.schulferien_org import SchulferienOrg, LOG


class Test():

    def setUp(self):
        self.s = SchulferienOrg()
        logging.getLogger().addHandler(logging.NullHandler())
        LOG.setLevel(logging.DEBUG)

    def tearDown(self):
        pass
