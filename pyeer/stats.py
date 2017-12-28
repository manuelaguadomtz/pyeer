# -*- coding:utf-8 -*-

import operator

import numpy as np

__copyright__ = 'Copyright 2017'
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
    # gscores = np.array(gscores) * -1
    # iscores = np.array(iscores) * -1

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

    # return thresholds * -1, fm_rates, fnm_rates
    return thresholds, fm_rates, fnm_rates


def calculate_roc_auc(fmr, fnmr):
    """Calculates the area under a ROC curve

    @param fmr: False Match Rates
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates
    @type fnmr: ndarray

    @returns: Area under the ROC curve
    @rtype: float
    """
    x1 = fmr[:-1]
    x2 = fmr[1:]

    tpr = 1 - fnmr
    y1 = tpr[:-1]
    y2 = tpr[1:]

    return ((x1 - x2) * (y1 + (y2 - y1) / 2)).sum()


def get_fnmr_op(fmr, fnmr, op):
    """Returns the value of the given FNMR operating point

    Definition:
    ZeroFNMR: is defined as the lowest FMR at which no non-false matches occur.

    Others FNMR operating points are defined in a similar way.

    @param fmr: False Match Rates
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates
    @type fnmr: ndarray
    @param op: Operating point
    @type op: float

    @returns: The lowest FMR at which the probability of FNMR == op
    @rtype: float
    """
    temp = abs(fnmr - op)
    min_val = np.min(temp)
    index = np.where(temp == min_val)[0][-1]
    return fmr[index]


def get_fmr_op(fmr, fnmr, op):
    """Returns the value of the given FMR operating point

    Definition:
    ZeroFMR: is defined as the lowest FNMR at which no false matches occur.

    Others FMR operating points are defined in a similar way.

    @param fmr: False Match Rates
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates
    @type fnmr: ndarray
    @param op: Operating point
    @type op: float

    @returns: The lowest FNMR at which the probability of FMR == op
    @rtype: float
    """
    index = np.argmin(abs(fmr - op))
    return fnmr[index]


def get_eer_values(fmr, fnmr):
    """Returns the value of the Equal Error Rate

    Equal Error Rate (EER): is the point where FNMR(t) = FMR(t).
    In practice the score distribution are not continuous so and interval
    is returned instead. The EER value will be set as the midpoint of
    this interval.

    The interval will be defined as:
    [EERlow, EERhigh] = min(fnmr[t], fmr[t]), max(fnmr[t], fmr[t])
    where t = argmin(abs(fnmr - fmr))

    The EER value is computed as (EERlow + EERhigh) / 2

    Reference:

    @param fmr: False Match Rates (FMR)
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates (FNMR)
    @type fnmr: ndarray
    @param op: Operation point
    @type op: float

    @returns: EERlow, EERhigh, EER
    @rtype: tuple
    """
    index = np.argmin(abs(fmr - fnmr))
    eer = np.abs(fnmr[index] + fmr[index]) / 2.0
    return min(fnmr[index], fmr[index]), max(fnmr[index], fmr[index]), eer
