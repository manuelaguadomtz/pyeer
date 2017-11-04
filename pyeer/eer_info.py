# -*- coding:utf-8 -*-

import argparse
from os.path import join
from collections import namedtuple

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

from stats import calculate_roc, calculate_roc_hist, calculate_roc_auc,\
    get_fmr_op, get_fnmr_op

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


Stats = namedtuple('Stats', ['thrs', 'fmr', 'fnmr', 'auc', 'eer', 'fmr0',
                             'fmr1000', 'fmr100', 'fnmr0', 'fnmr1000',
                             'fnmr100', 'gen_scores', 'imp_scores'])


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
                    help="Path to save the plots in the cases where the option"
                         " -s was specified")
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
                    help="The width of the plotted curves (default=5)")
    ap.add_argument("-ls", "--legend_font_size", required=False, default=15,
                    help="The size of the legend font (default=20)")
    ap.add_argument("-hb", "--distribution_bins", required=False, default=100,
                    help="The number of bins to compute scores distribution")
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
        index = np.argmin(abs(fmr - fnmr))
        eer = abs(fnmr[index] + fmr[index]) / 2.0

        # Estimating FMR operation points
        fmr0 = get_fmr_op(fmr, fnmr, 0)
        fmr1000 = get_fmr_op(fmr, fnmr, 0.001)
        fmr100 = get_fmr_op(fmr, fnmr, 0.01)

        # Estimating FNMR operation points
        fnmr0 = get_fnmr_op(fmr, fnmr, 0)
        fnmr1000 = get_fnmr_op(fmr, fnmr, 0.001)
        fnmr100 = get_fnmr_op(fmr, fnmr, 0.01)

        # Calculating area under the ROC curve
        auc = calculate_roc_auc(fmr, fnmr)

        # Stacking stats
        stats.append(Stats(thrs=thrs, fmr=fmr, fnmr=fnmr, auc=auc, eer=eer,
                           fmr0=fmr0, fmr100=fmr100, fmr1000=fmr1000,
                           fnmr0=fnmr0, fnmr100=fnmr100, fnmr1000=fnmr1000,
                           gen_scores=gen_scores, imp_scores=imp_scores))

    # Generating reports
    print('Generating report...')

    # TODO generating CSV

    print('Plotting...')

    # Preparing plots
    det_fig = plt.figure()
    det_plot = det_fig.add_subplot(111)
    det_plot.set_title('DET Curves')
    det_plot.grid(True)
    det_plot.set_ylabel('FNMR')
    det_plot.set_xlabel('FMR')

    roc_fig = plt.figure()
    roc_plot = roc_fig.add_subplot(111)
    roc_plot.set_title('ROC Curves')
    roc_plot.grid(True)
    roc_plot.set_ylabel('1 - FNMR')
    roc_plot.set_xlabel('FMR')
    roc_plot.plot([0, 1], [0, 1], 'k--', linewidth=line_width)

    for i, st in enumerate(stats):
        exp_id = experiments[i][2]

        # Plotting score distributions
        if not args.hist:
            title = 'Score distributions experiment: ' + exp_id
            dist_fig = plt.figure()
            dist_plot = dist_fig.add_subplot(111)
            dist_plot.grid(False)
            dist_plot.set_ylabel('Frequency')
            dist_plot.set_xlabel('Scores')
            dist_plot.set_title(title)
            dist_plot.hist(st.gen_scores, bins=bins, color='b',
                           label='Genuine distribution')
            dist_plot.hist(st.imp_scores, bins=bins, alpha=0.5, color='r',
                           label='Impostor distribution')
            dist_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

            if args.save_plots:
                fig_name = 'Distributions (%s)' % exp_id + ext
                dist_fig.savefig(join(args.save_path, fig_name), dpi=dpi)

        # Plotting FMR and FNMR curves
        eer_fig = plt.figure()
        eer_plot = eer_fig.add_subplot(111)
        eer_plot.grid(True)
        eer_plot.set_ylabel('Error')
        eer_plot.set_xlabel('Matching Scores')
        eer_plot.set_title('FMR and FNMR Curves')
        eer_plot.plot(st.thrs, st.fmr, linewidth=line_width,
                      label=exp_id + ' (FMR)')
        eer_plot.plot(st.thrs, st.fnmr, linewidth=line_width,
                      label=exp_id + ' (FNMR)')
        eer_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

        if args.save_plots:
            fig_name = 'FMR and FNMR curves of experiment: (%s)' % exp_id + ext
            eer_fig.savefig(join(args.save_path, fig_name), dpi=dpi)

        # Plotting DET Curve
        det_plot.plot(st.fmr, st.fnmr, label=exp_id, linewidth=line_width)

        # Plotting ROC Curve
        label = exp_id + ' AUC = %f' % st.auc
        roc_plot.plot(st.fmr, 1 - st.fnmr, label=label, linewidth=line_width)

    # Finalizing plots
    det_plot.legend(loc='best', prop=FontProperties(size=lgf_size))
    roc_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

    # Showing plots or saving plots
    if args.save_plots:
        # saving plots
        eer_fig.savefig(join(args.save_path, 'EER' + ext), dpi=dpi)
        det_fig.savefig(join(args.save_path, 'DET' + ext), dpi=dpi)
        roc_fig.savefig(join(args.save_path, 'ROC' + ext), dpi=dpi)

        # closing plots
        plt.close()
    else:
        plt.show()
