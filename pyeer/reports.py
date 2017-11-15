# -*- coding:utf-8 -*-

from os.path import join
import csv

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

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
        row = ['Experiment ID', 'GMean', 'GVariance', 'IMean',
               'IVariance', 'AUC', 'EERlow', 'EERhigh', 'EER',
               'FMR=0', 'FMR1000', 'FMR100', 'FMR20', 'FMR10',
               'FNMR0']
        writer.writerow(row)

        for st in stats:
            # Writing stats
            row = [st.exp_id.encode("utf-8"), st.gmean, st.gvar,
                   st.imean, st.ivar, st.auc, st.eer_low, st.eer_high,
                   st.eer, st.fmr0, st.fmr1000, st.fmr100, st.fmr20,
                   st.fmr10, st.fnmr0]
            writer.writerow(row)

        # Writing legend
        writer.writerow([])
        writer.writerow(['Legend:'])
        writer.writerow(['GMean: Genuine scores distribution mean'])
        writer.writerow(['GVariance: Genuine scores distribution variance'])
        writer.writerow(['IMean: Impostor scores distribution mean'])
        writer.writerow(['IVariance: Impostor scores distribution variance'])
        writer.writerow(['AUC: Area under the ROC curve'])
        writer.writerow(['EER: Equal Error Rate'])
        writer.writerow(['FMR: False Match Rate'])
        writer.writerow(['FNMR: False Non-Match Rate'])


def plot_stats(stats, line_width=3, hist_format=True, bins=100, lgf_size=15,
               log_plot=True, save_plots=False, dpi=None, save_path='',
               ext='.png'):
    """Plot a series of graphs from the given stats

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
    @param hist_format: Indicates whether the impostor scores are in
                        histogram format
    @type hist_format: bool
    @param bins: The number of bins to compute scores distribution
                 It will be ignored if the hist_format=True
    @type bins: int
    @param lgf_size: The size of the legend font (default=15)
    @type lgf_size: int
    @param log_plot: Indicates whether to plot the DET curves in a
                     log-log scale
    @type log_plot: bool
    @param save_plots: Indicates whether to save the plots instead
                       of showing them
    @type save_plots: bool
    @param dpi: Plots resolution (dots per inch) used when save_plots=True.
                If not given it will default to the value of savefig.dpi
                in the matplotlibrc file
    @type dpi: int
    @param save_path: Path to save the plots (if save_plots=True)
                      and stats report
    @type save_path: str
    @param ext: Format to save the plots if save_plots=True. Valid
                formats are: (.png, .pdf, .ps, .eps and .svg)
                (default='.png')
    @type ext: str
    """
    # Preparing plots
    det_fig = plt.figure()
    det_plot = det_fig.add_subplot(111)
    det_plot.set_title('DET Curves')
    det_plot.set_ylabel('FNMR')
    det_plot.set_xlabel('FMR')

    if log_plot:
        det_plot.set_yscale('log')
        det_plot.set_xscale('log')
        det_plot.grid(True, which='both', ls='--')
    else:
        det_plot.grid(True)

    roc_fig = plt.figure()
    roc_plot = roc_fig.add_subplot(111)
    roc_plot.set_title('ROC Curves')
    roc_plot.grid(True)
    roc_plot.set_ylabel('1 - FNMR')
    roc_plot.set_xlabel('FMR')
    roc_plot.plot([0, 1], [0, 1], 'k--', linewidth=line_width)

    for st in stats:
        # Plotting score distributions
        title = 'Score distributions experiment: ' + st.exp_id
        dist_fig = plt.figure()
        dist_plot = dist_fig.add_subplot(111)
        dist_plot.grid(False)
        dist_plot.set_ylabel('Frequency')
        dist_plot.set_xlabel('Scores')
        dist_plot.set_title(title)

        if hist_format:
            m = max(st.gen_scores)
            x = np.arange(m)
            ghist = np.histogram(st.gen_scores, bins=np.arange(m + 1))[0]
            dist_plot.plot(x, ghist, color='g',
                           label='Genuine scores %d' % len(st.gen_scores))

            x = np.arange(len(st.imp_scores))
            dist_plot.plot(x, st.imp_scores, color='r',
                           label='Impostor scores %d' % sum(st.imp_scores))
        else:
            dist_plot.hist(st.gen_scores, bins=bins, color='g',
                           label='Genuine scores %d' % len(st.gen_scores))
            dist_plot.hist(st.imp_scores, bins=bins, alpha=0.5, color='r',
                           label='Impostor scores %d' % len(st.imp_scores))

        dist_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

        if save_plots:
            fig_name = 'Distributions (%s)' % st.exp_id + ext
            dist_fig.savefig(join(save_path, fig_name), dpi=dpi)

        # Plotting FMR and FNMR curves
        eer_fig = plt.figure()
        eer_plot = eer_fig.add_subplot(111)
        eer_plot.grid(True)
        eer_plot.set_ylabel('Error')
        eer_plot.set_xlabel('Matching Scores')
        eer_plot.set_title('FMR and FNMR Curves')
        eer_plot.plot(st.thrs, st.fmr, linewidth=line_width,
                      label=st.exp_id + ' (FMR)')
        eer_plot.plot(st.thrs, st.fnmr, linewidth=line_width,
                      label=st.exp_id + ' (FNMR)')
        eer_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

        if save_plots:
            fname = 'FMR and FNMR curves of experiment: (%s)' % st.exp_id + ext
            eer_fig.savefig(join(save_path, fname), dpi=dpi)

        # Plotting DET Curve
        det_plot.plot(st.fmr, st.fnmr, label=st.exp_id, linewidth=line_width)

        # Plotting ROC Curve
        label = st.exp_id + ' AUC = %f' % st.auc
        roc_plot.plot(st.fmr, 1 - st.fnmr, label=label, linewidth=line_width)

    # Finalizing plots
    det_plot.legend(loc='best', prop=FontProperties(size=lgf_size))
    roc_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

    # Showing plots or saving plots
    if save_plots:
        # saving plots
        det_fig.savefig(join(save_path, 'DET' + ext), dpi=dpi)
        roc_fig.savefig(join(save_path, 'ROC' + ext), dpi=dpi)

        # closing plots
        plt.close()
    else:
        plt.show()
