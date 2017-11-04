# -*- coding:utf-8 -*-

import argparse
from os.path import join

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

from stats import calculate_roc, calculate_roc_hist, calculate_roc_auc,\
    get_fmr_op, get_fnmr_op

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


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

    for exp in experiments:
        # Printing experiment log header
        print('=' * (len(exp[2]) + 12))
        print('Experiment: ' + exp[2])
        print('=' * (len(exp[2]) + 12))

        # Loading scores
        print('Loading genuine scores file...')
        with open(join(args.path, exp[0])) as tf:
            gen_scores = [__get_score(line) for line in tf]

        print('Loading impostor scores file...')
        with open(join(args.path, exp[1])) as tf:
            imp_scores = [__get_score(line) for line in tf]

        print('Calculating stats...')
        if args.hist:
            # Calculating probabilities histogram format
            roc_info = calculate_roc_hist(gen_scores, imp_scores)
        else:
            # Calculating probabilities using scores as thrs
            roc_info = calculate_roc(gen_scores, imp_scores)

        # Unboxing probability rates and info
        thrs, fmr, fnmr = roc_info

        # Estimating EER
        print('...............................')

        index = np.argmin(abs(fmr - fnmr))
        eer = abs(fnmr[index] + fmr[index]) / 2.0
        print('EER       = ' + str(eer))

        print('..............................')

        # Estimating FMR operation points
        op = get_fmr_op(fmr, fnmr, 0)
        print('FMR_0     = ' + str(op))

        op = get_fmr_op(fmr, fnmr, 0.001)
        print('FMR_1000  = ' + str(op))

        op = get_fmr_op(fmr, fnmr, 0.01)
        print('FMR_100   = ' + str(op))

        print('...............................')

        # Estimating FNMR operation points
        op = get_fnmr_op(fmr, fnmr, 0)
        print('FNMR_0    = ' + str(op))

        op = get_fnmr_op(fmr, fnmr, 0.001)
        print('FNMR_1000 = ' + str(op))

        op = get_fnmr_op(fmr, fnmr, 0.01)
        print('FNMR_100  = ' + str(op))

        print('...............................')

        print('Ploting Curves...')

        # Plotting score distributions
        if not args.hist:
            dist_fig = plt.figure()
            dist_plot = dist_fig.add_subplot(111)
            dist_plot.grid(False)
            dist_plot.set_ylabel('Frequency')
            dist_plot.set_xlabel('Scores')
            dist_plot.set_title('Score distributions experiment: ' + exp[2])
            dist_plot.hist(gen_scores, bins=bins, color='b',
                           label='Genuine distribution')
            dist_plot.hist(imp_scores, bins=bins, alpha=0.5, color='r',
                           label='Impostor distribution')
            dist_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

            if args.save_plots:
                fig_name = 'Distributions (%s)' % exp[2] + ext
                dist_fig.savefig(join(args.save_path, fig_name), dpi=dpi)

        # Plotting FMR and FNMR curves
        eer_fig = plt.figure()
        eer_plot = eer_fig.add_subplot(111)
        eer_plot.grid(True)
        eer_plot.set_ylabel('Error')
        eer_plot.set_xlabel('Matching Scores')
        eer_plot.set_title('FMR and FNMR Curves')
        eer_plot.plot(thrs, fmr, linewidth=line_width, label=exp[2] + ' (FMR)')
        eer_plot.plot(thrs, fnmr, linewidth=line_width,
                      label=exp[2] + ' (FNMR)')

        if args.save_plots:
            fig_name = 'FMR and FNMR curves of experiment: (%s)' % exp[2] + ext
            eer_fig.savefig(join(args.save_path, fig_name), dpi=dpi)

        # Plotting DET Curve
        det_plot.plot(fmr, fnmr, label=exp[2], linewidth=line_width)

        # Calculating area under the ROC curve
        auc = calculate_roc_auc(fmr, fnmr)
        print('...............................')
        print('AUC = %f' % auc)
        print('...............................')

        # Plotting ROC Curve
        label = exp[2] + ' AUC = %f' % auc
        roc_plot.plot(fmr, 1 - fnmr, label=label, linewidth=line_width)

    # Finalizing plots
    eer_plot.legend(loc='best', prop=FontProperties(size=lgf_size))
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
