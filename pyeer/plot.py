from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


STYLES = ['s--', 'v--', 'o--', '^--', ',--', '<--', '>--', '1--', '2--'
          '3--', '4--', '.--', 'p--', '*--', 'h--', 'H--', '+--', 'x--'
          'd--', '|--', '---']


def __plt_det_curve(stats, ids, line_width=3, lgf_size=15, log_plot=True,
                    save_plots=False, dpi=None, save_path='', ext='.png'):
    """Plot the DET curve

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
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

    for i, st in enumerate(stats):
        # Plotting DET Curve
        det_plot.plot(st.fmr, st.fnmr, label=ids[i], linewidth=line_width)

    # Finalizing plots
    det_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

    # Showing plots or saving plots
    if save_plots:
        # saving plots
        det_fig.savefig(join(save_path, 'DET' + ext), dpi=dpi)


def __plt_roc_curve(stats, ids, line_width=3, lgf_size=15, log_plot=True,
                    save_plots=False, dpi=None, save_path='', ext='.png'):
    """Plot the ROC curve

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
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
    roc_fig = plt.figure()
    roc_plot = roc_fig.add_subplot(111)
    roc_plot.set_title('ROC Curves')
    roc_plot.grid(True)
    roc_plot.set_ylabel('1 - FNMR')
    roc_plot.set_xlabel('FMR')

    if log_plot:
        # roc_plot.set_yscale('log')
        roc_plot.set_xscale('log')
        roc_plot.grid(True, which='minor', ls='--')
    else:
        roc_plot.plot([0, 1], [0, 1], 'k--', linewidth=line_width)
        roc_plot.grid(True)

    for i, st in enumerate(stats):
        # Plotting ROC Curve
        label = ids[i] + ' AUC = %f' % st.auc
        roc_plot.plot(st.fmr, 1 - st.fnmr, label=label, linewidth=line_width)

    # Finalizing plots
    roc_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

    # Showing plots or saving plots
    if save_plots:
        # saving plots
        roc_fig.savefig(join(save_path, 'ROC' + ext), dpi=dpi)


def __plt_distributions(stats, ids, hformat=False, bins=100,
                        lgf_size=15, save_plots=False, dpi=None,
                        save_path='', ext='.png'):
    """Plot the scores distribution of each experiment

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param hformat: Indicates whether the impostor scores are in
                        histogram format
    @type hormat: bool
    @param bins: The number of bins to compute scores distribution
                 It will be ignored if the hist_format=True
    @type bins: int
    @param lgf_size: The size of the legend font (default=15)
    @type lgf_size: int
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
    for i, st in enumerate(stats):
        # Plotting score distributions
        title = 'Score distributions experiment: ' + ids[i]
        dist_fig = plt.figure()
        dist_plot = dist_fig.add_subplot(111)
        dist_plot.grid(False)
        dist_plot.set_ylabel('Frequency')
        dist_plot.set_xlabel('Scores')
        dist_plot.set_title(title)

        if hformat:
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
            fig_name = 'Distributions (%s)' % ids[i] + ext
            dist_fig.savefig(join(save_path, fig_name), dpi=dpi)


def __plt_error_curves(stats, ids, line_width=3, lgf_size=15, save_plots=False,
                       dpi=None, save_path='', ext='.png'):
    """Plot FMR and FNMR curves for each experiment

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
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
    for i, st in enumerate(stats):
        # Plotting FMR and FNMR curves
        eer_fig = plt.figure()
        eer_plot = eer_fig.add_subplot(111)
        eer_plot.grid(True)
        eer_plot.set_ylabel('Error')
        eer_plot.set_xlabel('Matching Scores')
        eer_plot.set_title('FMR and FNMR Curves')
        eer_plot.plot(st.thrs, st.fmr, linewidth=line_width,
                      label=ids[i] + ' (FMR)')
        eer_plot.plot(st.thrs, st.fnmr, linewidth=line_width,
                      label=ids[i] + ' (FNMR)')
        eer_plot.legend(loc='best', prop=FontProperties(size=lgf_size))

        if save_plots:
            fname = 'FMR and FNMR curves (%s)' % ids[i] + ext
            eer_fig.savefig(join(save_path, fname), dpi=dpi)


def plot_eer_stats(stats, ids, line_width=3, hformat=False, bins=100,
                   lgf_size=15, log_plot=True, save_plots=False, dpi=None,
                   save_path='', ext='.png'):
    """Plot a series of graphs from the given stats

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
    @param hformat: Indicates whether the impostor scores are in
                        histogram format
    @type hormat: bool
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
    # Plotting the DET curve
    __plt_det_curve(stats, ids, line_width, lgf_size, log_plot, save_plots,
                    dpi, save_path, ext)

    # Plotting the ROC curve
    __plt_roc_curve(stats, ids, line_width, lgf_size, log_plot, save_plots,
                    dpi, save_path, ext)

    # Plotting scores distribution
    __plt_distributions(stats, ids, hformat, bins, lgf_size, save_plots,
                        dpi, save_path, ext)

    # Plotting error curves
    __plt_error_curves(stats, ids, line_width, lgf_size, save_plots,
                       dpi, save_path, ext)

    # Showing plots or saving plots
    if save_plots:
        # closing plots
        plt.close('all')
    else:
        plt.show()


def plot_cmc_stats(stats, max_rank, line_width=3, lgf_size=15,
                   save_plots=False, dpi=None, save_path='.', ext='.png'):
    """Plot a series of graphs from the given stats

    @param stats: An iterable with instances of the named tuple CMCstats
    @type stats: iterable
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param line_width: The width of the plotted curves (default=3)
    @type line_width: int
    @param lgf_size: The size of the legend font (default=15)
    @type lgf_size: int
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
    plt.title('CMC Curves')
    plt.ylabel('Accuracy')
    plt.xlabel('Rank')
    plt.grid(True)
    plt.axis(xmin=1, xmax=max_rank)
    plt.xticks(range(1, max_rank))

    for i, st in enumerate(stats):
        plt.plot(range(1, len(st.ranks) + 1), st.ranks, STYLES[i],
                 label=st.exp_id, linewidth=line_width)

    # Finalizing plots
    plt.legend(loc='best', prop=FontProperties(size=lgf_size))

    # Showing plots or saving plots
    if save_plots:
        # saving plots
        plt.savefig(join(save_path, 'CMC' + ext), dpi=dpi)

        # closing plots
        plt.close()
    else:
        plt.show()
