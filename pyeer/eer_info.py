# -*- coding:utf-8 -*-

import argparse

from os.path import join, isdir, basename
from os import listdir

import numpy as np

from .eer_stats import calculate_roc, calculate_roc_hist, calculate_roc_auc,\
    get_fmr_op, get_fnmr_op, get_eer_values, Stats, get_decidability_value,\
    get_youden_index, get_matthews_ccoef
from .report import generate_eer_report, export_error_rates
from .plot import plot_eer_stats

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


def __get_files(base_path, arg_val):
    """ Get the file names from the argument value

    @param base_path: The path where the files are suppose to be
    @type base_path: str
    @param arg_val: The argument value of genuine or impostor scores files
    @type arg_val: str
    """
    if isdir(join(base_path, arg_val)):
        files = sorted(listdir(join(base_path, arg_val)))
        return [join(arg_val, f) for f in files]
    else:
        return [f.strip() for f in arg_val.split(',')]


def __get_score(line):
    """Get the score value from an input score file line

    @param line: An input score file line
    @type line: str

    @returns: The parsed score
    @rtype: float
    """
    sline = line.strip().split(' ')
    return float(sline[-1])


def get_eer_info_cmd():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False, default='.',
                    help="The path to the scores files. (Default='.')")
    ap.add_argument("-i", "--iscores_files", required=True,
                    help="The impostor scores files. Multiple files must be"
                         " separated by a comma. Instead of the filenames, a"
                         " directory relative to PATH could be given. In this"
                         " case, it is strongly recommended that genuine"
                         " scores files are specified in the same way and that"
                         " corresponding pairs of scores files (genuine and"
                         " impostor) have the same name.")
    ap.add_argument("-g", "--gscores_files", required=True,
                    help="The genuine scores files. Multiple files must be"
                         " separated by a comma. Instead of the filenames, a"
                         " directory relative to PATH could be given. In this"
                         " case, it is strongly recommended that impostor"
                         " scores files are specified in the same way and that"
                         " corresponding pairs of scores files (genuine and"
                         " impostor) have the same name.")
    ap.add_argument("-e", "--experiment_ids", required=False,
                    help="Experiment ID. Multiple IDs must be separated by"
                         " a comma. If not given, genuine score file names"
                         " will be used to identified each experiment")
    ap.add_argument("-ht", "--hist", required=False, action='store_true',
                    help="Indicates that the impostor file is in histogram"
                         " format")
    ap.add_argument("-ds", "--ds_scores", required=False, action='store_true',
                    help="Indicates that the input scores are dissimilarity"
                         " scores")
    ap.add_argument("-hb", "--distribution_bins", required=False, default=100,
                    help="The number of bins to compute scores distributions."
                         " Will be ignored if -ht is passed as parameter"
                         " (default=100)")
    ap.add_argument("-np", "--no_plots", required=False, action='store_true',
                    help="Indicates whether to not plot the results")
    ap.add_argument("-sp", "--save_path", required=False, default='',
                    help="Path to save plots and stats reports")
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
    ap.add_argument("-lw", "--line_width", required=False, default=3,
                    help="Line width for plots (default=3)")
    ap.add_argument("-ls", "--legend_font_size", required=False, default=15,
                    help="The size of the plots legend font (default=15)")
    args = ap.parse_args()

    # Parsing arguments
    gscores_files = __get_files(args.path, args.gscores_files)
    iscores_files = __get_files(args.path, args.iscores_files)

    experiment_ids = ([e.strip() for e in args.experiment_ids.split(',')]
                      if args.experiment_ids else
                      [basename(name) for name in gscores_files])

    experiments = zip(gscores_files, iscores_files, experiment_ids)

    # Plot arguments
    line_width = int(args.line_width)
    lgf_size = int(args.legend_font_size)
    dpi = None if args.save_dpi is None else int(args.save_dpi)
    ext = '.' + args.plots_format
    bins = int(args.distribution_bins)

    # Experiment stats
    stats = []
    ids = []

    for exp in experiments:
        # Loading scores
        print('%s: Loading genuine scores file...' % exp[2])
        with open(join(args.path, exp[0])) as tf:
            gen_scores = [__get_score(line) for line in tf]

        print('%s: Loading impostor scores file...' % exp[2])
        with open(join(args.path, exp[1])) as tf:
            imp_scores = [__get_score(line) for line in tf]

        print('%s: Calculating stats...' % exp[2])
        exp_stats = get_eer_stats(gen_scores, imp_scores,
                                  args.hist, args.ds_scores)
        stats.append(exp_stats)
        ids.append(exp[2])

    # Generating reports
    print('Generating report...')

    filename = join(args.save_path, 'pyeer_report.' + args.report_format)
    generate_eer_report(stats, ids, filename)

    # Exporting error rates
    for i, st in enumerate(stats):
        filename = join(args.save_path, ids[i] + ' (Rates).csv')
        export_error_rates(st.fmr, st.fnmr, filename)

    if not args.no_plots:
        print('Plotting...')
        plot_eer_stats(stats, ids, line_width, args.hist, bins, lgf_size,
                       True, dpi, args.save_path, ext)


def get_eer_stats(gen_scores, imp_scores, hformat=False, ds_scores=False):
    """Calculates EER associated statistics

    Keyword Arguments:
    @param gen_scores: The genuine scores
    @type gen_scores: list
    @param imp_scores: The impostor scores
    @type imp_scores: list
    @param id: An id for the experiment
    @type id: str
    @param hformat: Indicates whether the impostor scores are in histogram
        format
    @type hformat: bool
    @param ds_scores: Indicates whether the input scores are dissimilarity
        scores
    @type ds_scores: bool
    """
    if hformat:
        # Calculating probabilities histogram format
        roc_info = calculate_roc_hist(gen_scores, imp_scores,
                                      ds_scores, rates=False)
        gnumber = float(len(gen_scores))
        inumber = float(sum(imp_scores))
    else:
        # Calculating probabilities using scores as thrs
        roc_info = calculate_roc(gen_scores, imp_scores,
                                 ds_scores, rates=False)
        gnumber = len(gen_scores)
        inumber = len(imp_scores)

    # Unboxing probability rates and info
    thrs, fm, fnm = roc_info
    fmr = fm / inumber
    fnmr = fnm / gnumber

    # Estimating EER
    eer_ind, eer_low, eer_high, eer = get_eer_values(fmr, fnmr)
    eer_th = thrs[eer_ind]

    # Estimating FMR operating points
    ind, fmr0 = get_fmr_op(fmr, fnmr, 0)
    fmr0_th = thrs[ind]

    ind, fmr1000 = get_fmr_op(fmr, fnmr, 0.001)
    fmr1000_th = thrs[ind]

    ind, fmr100 = get_fmr_op(fmr, fnmr, 0.01)
    fmr100_th = thrs[ind]

    ind, fmr20 = get_fmr_op(fmr, fnmr, 0.05)
    fmr20_th = thrs[ind]

    ind, fmr10 = get_fmr_op(fmr, fnmr, 0.1)
    fmr10_th = thrs[ind]

    # Estimating FNMR operating points
    ind, fnmr0 = get_fnmr_op(fmr, fnmr, 0)
    fnmr0_th = thrs[ind]

    # Calculating distributions mean and variance
    gmean = np.mean(gen_scores)
    gstd = np.std(gen_scores)

    if hformat:
        nscores = sum(imp_scores)
        nscores_prob = np.array(imp_scores) / nscores
        scores = np.arange(len(imp_scores))

        imean = (scores * nscores_prob).sum()
        istd = np.sqrt(((scores - imean) ** 2 * nscores_prob).sum())
    else:
        imean = np.mean(imp_scores)
        istd = np.std(imp_scores)

    dec = get_decidability_value(gmean, gstd, imean, istd)

    # Calculating area under the ROC curve
    auc = calculate_roc_auc(fmr, fnmr)

    j_index, j_index_th = get_youden_index(fmr, fnmr)
    j_index_th = thrs[j_index_th]

    mccoef, mccoef_th = get_matthews_ccoef(fm, fnm, gnumber, inumber)
    mccoef_th = thrs[mccoef_th]

    # Stacking stats
    return Stats(thrs=thrs, fmr=fmr, fnmr=fnmr, auc=auc, eer=eer,
                 fmr0=fmr0, fmr100=fmr100, fmr1000=fmr1000,
                 fmr20=fmr20, fmr10=fmr10, fnmr0=fnmr0,
                 gen_scores=gen_scores, imp_scores=imp_scores,
                 gmean=gmean, gstd=gstd, imean=imean, istd=istd,
                 eer_low=eer_low, eer_high=eer_high, decidability=dec,
                 j_index=j_index, j_index_th=j_index_th, eer_th=eer_th,
                 mccoef=mccoef, mccoef_th=mccoef_th, fmr0_th=fmr0_th,
                 fmr1000_th=fmr1000_th, fmr100_th=fmr100_th,
                 fmr20_th=fmr20_th, fmr10_th=fmr10_th, fnmr0_th=fnmr0_th)
