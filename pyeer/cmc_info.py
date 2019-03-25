# -*- coding:utf-8 -*-

import argparse

from os.path import join

from .cmc_stats import load_scores_from_file, get_cmc_curve, CMCstats
from .report import generate_cmc_report
from .plot import plot_cmc_stats

__copyright__ = 'Copyright 2017'
__author__ = u'Manuel Aguado Martínez'


def get_cmc_info():
    # Setting script arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False, default='.',
                    help="The path to the scores files")
    ap.add_argument("-ms", "--scores_filenames", required=True,
                    help="The scores file. Multiple files must be"
                         " separated by a comma")
    ap.add_argument("-t", "--true_pairs_file_names", required=True,
                    help="Genuine pairs file. Multiple files must be"
                         " separated by a comma.")
    ap.add_argument("-e", "--experiment_names", required=True,
                    help="Experiment ID. Multiple IDS must be separated by "
                         " comma")
    ap.add_argument("-r", "--maximum_rank", required=False, default=20,
                    help="The maximum rank to calculate the penetration"
                         " coefficient. (default=20)")
    ap.add_argument("-lw", "--line_width", required=False, default=2,
                    help="Line width for plots (default=2)")
    ap.add_argument("-lf", "--legend_font", required=False, default=12,
                    help="The size of the plots legend font (default=12)")
    ap.add_argument("-np", "--no_plots", required=False, action='store_true',
                    help="Indicates whether to not plot the results")
    ap.add_argument("-sp", "--save_path", required=False, default='',
                    help="Path to save the plots (if -s was specified)"
                         " and stats report")
    ap.add_argument("-pf", "--plots_format", required=False, default='png',
                    help="Format to save plots. Valid formats are:"
                         "(png, pdf, ps, eps and svg)")
    ap.add_argument("-rf", "--report_format", required=False, default='csv',
                    help="Format to save the report. Valid formats are:"
                         " (csv, html, tex, json). Default csv.")
    ap.add_argument("-sr", "--save_dpi", required=False, default=None,
                    help="Plots resolution (dots per inch). If not given"
                         " it will default to the value savefig.dpi in the"
                         " matplotlibrc file")
    ap.add_argument("-ds", "--ds_scores", required=False, action='store_true',
                    help='Indicates whether the input scores are dissimilarity'
                         'scores')
    args = ap.parse_args()

    # Parsing script arguments
    score_filenames = args.scores_filenames.split(',')
    true_pairs_filenames = args.true_pairs_file_names.split(',')
    if len(true_pairs_filenames) == 1:
        true_pairs_filenames *= len(score_filenames)
    experiment_names = args.experiment_names.split(',')
    experiments = zip(score_filenames, true_pairs_filenames, experiment_names)
    rank = int(args.maximum_rank)
    line_width = int(args.line_width)
    lgf_size = int(args.legend_font)
    ext = '.' + args.plots_format
    dpi = None if args.save_dpi is None else int(args.save_dpi)

    # Calculating CMC values for each experiment and plotting them
    stats = []
    for i, exp in enumerate(experiments):
        s_filename = join(args.path, exp[0])
        tp_filename = join(args.path, exp[1])
        experiment_name = exp[2]

        print('%s: Loading scores file...' % experiment_name)
        scores = load_scores_from_file(s_filename, tp_filename, args.ds_scores)

        print('%s: Calculating CMC cruve...' % experiment_name)
        rank_values = get_cmc_curve(scores, rank)

        stats.append(CMCstats(exp_id=experiment_name, ranks=rank_values))

    # Generating reports
    print('Generating report...')

    filename = join(args.save_path, 'pyeer_report.' + args.report_format)
    generate_cmc_report(stats, rank, filename)

    if not args.no_plots:
        print('Plotting...')
        plot_cmc_stats(stats, rank, line_width, lgf_size, True,
                       dpi, args.save_path, ext)
