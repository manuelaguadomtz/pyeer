# -*- coding:utf-8 -*-

import csv
import pkg_resources

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


def generate_csv_eer_report(stats, ids, save_file):
    """ Generate a CSV file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Writing headers
        writer = csv.writer(sf)

        # Writing package version
        pkg_version = pkg_resources.require('pyeer')[0].version
        writer.writerow(['Generated using PyEER ' + pkg_version])

        row = ['Experiment ID', 'GMean', 'GSTD', 'IMean',
               'ISTD', "Sensitivity index (d')", 'AUC', 'J-Index',
               'J-Index_TH', 'MCC', 'MCC_TH', 'EERlow',
               'EERhigh', 'EER', 'ZeroFMR', 'FMR1000', 'FMR100',
               'FMR20', 'FMR10', 'ZeroFNMR', 'EER_TH', 'ZeroFMR_TH',
               'FMR1000_TH', 'FMR100_TH', 'FMR20_TH', 'FMR10_TH',
               'ZeroFNMR_TH']
        writer.writerow(row)

        for i, st in enumerate(stats):
            # Writing stats
            row = [ids[i], st.gmean, st.gstd, st.imean, st.istd,
                   st.decidability, st.auc, st.j_index, st.j_index_th,
                   st.mccoef, st.mccoef_th, st.eer_low, st.eer_high,
                   st.eer, st.fmr0, st.fmr1000, st.fmr100, st.fmr20,
                   st.fmr10, st.fnmr0, st.eer_th, st.fmr0_th, st.fmr1000_th,
                   st.fmr100_th, st.fmr20_th, st.fmr10_th, st.fnmr0_th]
            writer.writerow(row)

        # Writing legend
        writer.writerow([])
        writer.writerow(['Legend:'])
        writer.writerow(['GMean: Genuine scores distribution mean'])
        writer.writerow(['GSTD: Genuine scores distribution '
                         'standard deviation'])
        writer.writerow(['IMean: Impostor scores distribution mean'])
        writer.writerow(['IVariance: Impostor scores distribution '
                         'standard deviation'])
        writer.writerow(["Sensitivity index (d'): See NICE:II protocol"
                         " evaluation"])
        writer.writerow(['AUC: Area under the ROC curve'])
        writer.writerow(["J-Index: Youden's J statistic (Youden's Index)"])
        writer.writerow(["MCC: Matthews Correlation Coefficient"])
        writer.writerow(['EER: Equal Error Rate'])
        writer.writerow(['EERlow, EERhigh: See FVC2000 protocol evaluation'])
        writer.writerow(['FMR: False Match Rate'])
        writer.writerow(['FNMR: False Non-Match Rate'])
        writer.writerow(['_TH: Threshold'])
        writer.writerow(['EER_TH: Threshold for which EERlow and EERHigh were'
                         ' calculated'])

        writer.writerow([])

        # Writing rates header
        headers = []
        max_nthrs = -1
        for i, st in enumerate(stats):
            headers += [' ', ids[i] + ' (FMR)', ids[i] + ' (FNMR)']

            nthrs = len(st.thrs)
            if nthrs > max_nthrs:
                max_nthrs = nthrs
        writer.writerow(headers)

        # Writing rates
        for i in range(max_nthrs):
            row = []
            for st in stats:
                if i < len(st.thrs):
                    row += [' ', st.fmr[i], st.fnmr[i]]
                else:
                    row += [' ', ' ', ' ']
            writer.writerow(row)


def generate_eer_report(stats, ids, save_file):
    """Writes EER statistics to a file

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report.
        The file format will depend on the filename extension.
    @type save_file: str
    """

    # Getting file extension
    ext = save_file.split('.')[-1]

    if ext.lower() == 'csv':
        generate_csv_eer_report(stats, ids, save_file)
    else:
        raise ValueError('Unsupported file format')


def generate_csv_cmc_report(stats, max_rank, save_file):
    """ Generate a CSV file with the given CMC rank values

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Writing headers
        writer = csv.writer(sf)
        row = ['Rank-' + str(i) for i in range(1, max_rank + 1)]
        writer.writerow(['Experiment ID'] + row)

        for st in stats:
            # Writing rank values
            writer.writerow([st.exp_id] + st.ranks)


def generate_cmc_report(stats, max_rank, save_file):
    """ Writes CMC rank values to a file

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report.
        The file format will depend on the filename extension.
    @type save_file: str
    """
    # Getting file extension
    ext = save_file.split('.')[-1]

    if ext.lower() == 'csv':
        generate_csv_cmc_report(stats, max_rank, save_file)
    else:
        raise ValueError('Unsupported file format')
