# -*- coding:utf-8 -*-

import csv

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


def generate_report(stats, save_file):
    """ Generate a CSV file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Writing headers
        writer = csv.writer(sf)
        row = ['Experiment ID', 'AUC', 'EER', 'FMR0', 'FMR1000',
               'FMR100', 'FNMR0', 'FNMR1000', 'FNMR100']
        writer.writerow(row)

        for st in stats:
            # Writing stats
            row = [st.exp_id.encode("utf-8"), st.auc, st.eer, st.fmr0,
                   st.fmr1000, st.fmr100, st.fnmr0, st.fnmr1000, st.fnmr100]
            writer.writerow(row)
