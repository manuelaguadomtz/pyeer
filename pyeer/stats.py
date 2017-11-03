# -*- coding:utf-8 -*-

import operator

import numpy as np

__copyright__ = 'Copyright 2016'
__author__ = u'Bsc. Manuel Aguado Martínez'


def calculate_roc_hist(gscores, iscores):
    """Calculates FMR, FNMR for impostor scores in histogram format

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list

    @return: (thresholds, FMR, FNMR)
    @rtype: tuple
    """
    match_thr = 0
    maximum_thr = max(max(gscores), len(iscores))

    gscores_number = float(len(gscores))
    iscores_number = float(sum(iscores))
    iscores = np.cumsum(iscores)

    thresholds = []
    fm_rates = []
    fnm_rates = []

    while match_thr <= maximum_thr:
        if 0 < match_thr < len(iscores):
            false_match = iscores_number - iscores[match_thr - 1]
        elif match_thr == 0:
            false_match = iscores_number  # Accepting everyone
        else:
            false_match = 0

        fm_rates.append(false_match / iscores_number)

        # List convertion for Python3 compatibility
        fnm = len(list(filter(lambda s: s < match_thr, gscores)))
        fnm_rates.append(fnm / gscores_number)

        thresholds.append(match_thr)
        match_thr += 1

    fm_rates = np.array(fm_rates)
    fnm_rates = np.array(fnm_rates)

    return thresholds, fm_rates, fnm_rates


def calculate_roc(gscores, iscores):
    """Calculates FMR, FNMR

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list

    @return: (thresholds, FMR, FNMR)
    @rtype: tuple
    """
    gscores_number = len(gscores)
    iscores_number = len(iscores)

    # Labeling genuine scores as 1 and impostor scores as 0
    gscores = zip(gscores, [1] * gscores_number)
    iscores = zip(iscores, [0] * iscores_number)

    # Python3 compatibility
    gscores = list(gscores)
    iscores = list(iscores)

    # Stacking scores
    scores = np.array(sorted(gscores + iscores, key=operator.itemgetter(0)))
    cumul = np.cumsum(scores[:, 1])

    # Grouping scores
    thresholds, u_indices = np.unique(scores[:, 0], return_index=True)

    # Calculating FNM and FM distributions
    fnm = cumul[u_indices] - scores[u_indices][:, 1]  # rejecting s < t
    fm = iscores_number - (u_indices - fnm)

    # Calculating FMR and FNMR
    fnm_rates = fnm / gscores_number
    fm_rates = fm / iscores_number

    return thresholds, fm_rates, fnm_rates
