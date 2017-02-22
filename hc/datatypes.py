# -*- coding: utf-8 -*-

"""
Data types definition
"""


class PhData(list):
    pass


class MonthDayList(list):
    pass


def fix_ph_data(dataset):
    for ph_name in dataset:
        dataset[ph_name] = PhData(dataset[ph_name])


def fix_data_types(dataset):

    if 'PH' in dataset:
        fix_ph_data(dataset['PH'])

    for entry in dataset:
        if 'PH' in dataset[entry]:
            fix_ph_data(dataset[entry]['PH'])
