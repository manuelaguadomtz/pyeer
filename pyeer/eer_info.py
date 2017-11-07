# -*- coding:utf-8 -*-

import argparse
from os.path import join
from collections import namedtuple

import numpy as np

from stats import calculate_roc, calculate_roc_hist, calculate_roc_auc,\
    get_fmr_op, get_fnmr_op, get_eer_values
from reports import generate_report, plot_stats

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


Stats = namedtuple('Stats', ['thrs', 'fmr', 'fnmr', 'auc', 'eer', 'fmr0',
                             'fmr100000', 'fmr10000', 'fmr1000', 'fmr100',
                             'fnmr0', 'fnmr100000', 'fnmr10000', 'fnmr1000',
                             'fnmr100', 'gen_scores', 'imp_scores', 'gmean',
                             'gvar', 'imean', 'ivar', 'exp_id', 'eer_low',
                             'eer_high'])


def __get_score(line):
    """Get the score value from an input score file line

    @param line: An input score file line
    @type line: str

    @returns: The parsed score
    @rtype: float
    """
    sline = line.strip().split(' ')
    return float(sline[-1])


def get_eer_info():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="path to exp files")
    ap.add_argument("-i", "--iscores_files", required=True,
                    help="Impostor exp file names separated by comma")
    ap.add_argument("-g", "--gscores_files", required=True,
                    help="Genuine exp file names separated by comma")
    ap.add_argument("-e", "--experiment_ids", required=True,
                    help="Experiment names separated by comma")
    ap.add_argument("-ht", "--hist", required=False, action='store_true',
                    help="Indicates that the impostor file is in"
                         "histogram format")
    ap.add_argument("-s", "--save_plots", required=False, action='store_true',
                    help="Indicates whether to save the plots instead of"
                         " showing them")
    ap.add_argument("-sp", "--save_path", required=False, default='',
                    help="Path to save the plots (if -s was specified)"
                         " and stats report")
    ap.add_argument("-sf", "--save_format", required=False, default='png',
                    help="Format to save the plots in the cases where the"
                         " option -s was specified. Valid formats are: "
                         "(png, pdf, ps, eps and svg)")
    ap.add_argument("-sr", "--save_dpi", required=False, default=None,
                    help="Plots resolution (dots per inch) in the cases"
                         " where the option -s was specified. If not given"
                         " it will default to the value savefig.dpi in the"
                         " matplotlibrc file")
    ap.add_argument("-lw", "--line_width", required=False, default=3,
                    help="The width of the plotted curves (default=3)")
    ap.add_argument("-ls", "--legend_font_size", required=False, default=15,
                    help="The size of the legend font (default=15)")
    ap.add_argument("-hb", "--distribution_bins", required=False, default=100,
                    help="The number of bins to compute scores distribution."
                         "Will be ignored if -ht is passed as parameter")
    args = ap.parse_args()

    # Parsing arguments
    gscores_files = [f.strip() for f in args.gscores_files.split(',')]
    iscores_files = [f.strip() for f in args.iscores_files.split(',')]
    experiment_ids = [e.strip() for e in args.experiment_ids.split(',')]
    experiments = zip(gscores_files, iscores_files, experiment_ids)
    line_width = int(args.line_width)
    lgf_size = int(args.legend_font_size)
    dpi = None if args.save_dpi is None else int(args.save_dpi)
    ext = '.' + args.save_format
    bins = int(args.distribution_bins)

    # Experiment stats
    stats = []

    for exp in experiments:
        # Loading scores
        print('%s: Loading genuine scores file...' % exp[2])
        with open(join(args.path, exp[0])) as tf:
            gen_scores = [__get_score(line) for line in tf]

        print('%s: Loading impostor scores file...' % exp[2])
        with open(join(args.path, exp[1])) as tf:
            imp_scores = [__get_score(line) for line in tf]

        print('%s: Calculating stats...' % exp[2])
        if args.hist:
            # Calculating probabilities histogram format
            roc_info = calculate_roc_hist(gen_scores, imp_scores)
        else:
            # Calculating probabilities using scores as thrs
            roc_info = calculate_roc(gen_scores, imp_scores)

        # Unboxing probability rates and info
        thrs, fmr, fnmr = roc_info

        # Estimating EER
        eer_low, eer_high, eer = get_eer_values(fmr, fnmr)

        # Estimating FMR operation points
        fmr0 = get_fmr_op(fmr, fnmr, 0)
        fmr100000 = get_fmr_op(fmr, fnmr, 0.00001)
        fmr10000 = get_fmr_op(fmr, fnmr, 0.0001)
        fmr1000 = get_fmr_op(fmr, fnmr, 0.001)
        fmr100 = get_fmr_op(fmr, fnmr, 0.01)

        # Estimating FNMR operation points
        fnmr0 = get_fnmr_op(fmr, fnmr, 0)
        fnmr100000 = get_fnmr_op(fmr, fnmr, 0.00001)
        fnmr10000 = get_fnmr_op(fmr, fnmr, 0.0001)
        fnmr1000 = get_fnmr_op(fmr, fnmr, 0.001)
        fnmr100 = get_fnmr_op(fmr, fnmr, 0.01)

        # Calculating distributions mean and variance
        gmean = np.mean(gen_scores)
        gvar = np.var(gen_scores)

        if args.hist:
            nscores = sum(imp_scores)
            nscores_prob = np.array(imp_scores) / nscores
            scores = np.arange(len(imp_scores))

            imean = (scores * nscores_prob).sum()
            ivar = ((scores - imean) ** 2 * nscores_prob).sum()
        else:
            imean = np.mean(imp_scores)
            ivar = np.var(imp_scores)

        # Calculating area under the ROC curve
        auc = calculate_roc_auc(fmr, fnmr)

        # Stacking stats
        stats.append(Stats(thrs=thrs, fmr=fmr, fnmr=fnmr, auc=auc, eer=eer,
                           fmr0=fmr0, fmr100=fmr100, fmr1000=fmr1000,
                           fnmr0=fnmr0, fnmr1000=fnmr1000, fnmr100=fnmr100,
                           gen_scores=gen_scores, imp_scores=imp_scores,
                           exp_id=exp[2], fmr10000=fmr10000,
                           fnmr10000=fnmr10000, fmr100000=fmr100000,
                           fnmr100000=fnmr100000, gmean=gmean, gvar=gvar,
                           imean=imean, ivar=ivar, eer_low=eer_low,
                           eer_high=eer_high))

    # Generating reports
    print('Generating report...')

    generate_report(stats, join(args.save_path, 'pyeer_report.csv'))

    print('Plotting...')

    plot_stats(stats, line_width, args.hist, bins, lgf_size,
               args.save_plots, dpi, args.save_path, ext)
