# -*- coding:utf-8 -*-

import operator

from collections import namedtuple

import numpy as np


__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


Stats = namedtuple('Stats', ['exp_id',  # Exp id

                             # Rate curves
                             'thrs',  # Thresholds
                             'fmr',  # False match rates
                             'fnmr',  # False non-match rates
                             'auc',  # Area under the ROC curve

                             # Operation points
                             'fmr0',  # Zero false math rate
                             'fmr1000',  # 1000 false match rate
                             'fmr100',  # 100 false match rate
                             'fmr20',  # 20 false match rate
                             'fmr10',  # 10 false match rate
                             'fnmr0',  # 0 false non-match rate

                             # Scores distributions
                             'gen_scores',  # Genuine scores
                             'imp_scores',  # Impostor scores
                             'gmean',  # Genuine scores mean
                             'gstd',  # Genuine scores standard deviation
                             'imean',  # Impostor scores mean
                             'istd',  # Impostor scores standard deviation
                             'decidability',  # Decidability score

                             # Values of EER
                             'eer',  # Equal error rate
                             'eer_low',  # Equal error rate (low)
                             'eer_high'  # Equal error rate (high)
                             ])


def calculate_roc_hist(gscores, iscores, ds_scores=False):
    """Calculates FMR, FNMR for impostor scores in histogram format

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list
    @param ds_scores: Indicates whether input scores are
        dissimilarity scores
    @type ds_scores: bool

    @return: (thresholds, FMR, FNMR)
    @rtype: tuple
    """
    match_thr = 0
    maximum_thr = max([max(gscores), len(gscores),
                       max(iscores), len(iscores)])

    gscores_number = float(len(gscores))
    iscores_number = float(sum(iscores))
    iscores = np.cumsum(iscores)

    thresholds = []
    fm_rates = []
    fnm_rates = []

    while match_thr <= maximum_thr:
        if 0 < match_thr < len(iscores):
            if ds_scores:
                false_match = iscores[match_thr - 1]
            else:
                false_match = iscores_number - iscores[match_thr - 1]
        elif match_thr == 0:
            if ds_scores:
                false_match = 0
            else:
                false_match = iscores_number  # Accepting everyone
        else:
            if ds_scores:
                false_match = iscores_number
            else:
                false_match = 0

        fm_rates.append(false_match / iscores_number)

        # List convertion for Python3 compatibility
        if ds_scores:
            fnm = len(list(filter(lambda s: s > match_thr, gscores)))
        else:
            fnm = len(list(filter(lambda s: s < match_thr, gscores)))
        fnm_rates.append(fnm / gscores_number)

        thresholds.append(match_thr)
        match_thr += 1

    fm_rates = np.array(fm_rates)
    fnm_rates = np.array(fnm_rates)

    return thresholds, fm_rates, fnm_rates


def calculate_roc(gscores, iscores, ds_scores=False):
    """Calculates FMR, FNMR

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list
    @param ds_scores: Indicates whether input scores are
        dissimilarity scores
    @type ds_scores: bool

    @return: (thresholds, FMR, FNMR)
    @rtype: tuple
    """
    if ds_scores:
        gscores = np.array(gscores) * -1
        iscores = np.array(iscores) * -1

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

    if ds_scores:
        return thresholds * -1, fm_rates, fnm_rates

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
    Maio, D., Maltoni, D., Cappelli, R., Wayman, J. L., & Jain, A. K. (2002).
    FVC2000: Fingerprint verification competition. IEEE Transactions on
    Pattern Analysis and Machine Intelligence, 24(3), 402-412.

    @param fmr: False Match Rates (FMR)
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates (FNMR)
    @type fnmr: ndarray
    @param op: Operation point
    @type op: float

    @returns: EERlow, EERhigh, EER
    @rtype: tuple
    """
    diff = fmr - fnmr
    t2 = np.where(diff <= 0)[0][0]
    t1 = t2 - 1 if diff[t2] != 0 and t2 != 0 else t2

    if fmr[t1] + fnmr[t1] <= fmr[t2] + fnmr[t2]:
        return fnmr[t1], fmr[t1], (fnmr[t1] + fmr[t1]) / 2
    else:
        return fmr[t2], fnmr[t2], (fnmr[t2] + fmr[t2]) / 2

    # index = np.argmin(abs(fmr - fnmr))
    # eer = np.abs(fnmr[index] + fmr[index]) / 2.0
    # return min(fnmr[index], fmr[index]), max(fnmr[index], fmr[index]), eer


def get_decidability_value(gmean, gstd, imean, istd):
    """ The decidability score (d') or decision-making powerused in NICE:II
    evauation protocol for iris, it is a measure of the separation between
    genuine and impostor distributions. Higher d' values indicate better
    separation

    @param gmean: The mean value of the genuine scores
    @type gmean: float
    @param imean: The mean value of the impostor scores
    @type imean: float
    @param gstd: The standard deviation value of the genuine scores
    @type gstd: float
    @param istd: The standard deviation value of the impostor scores
    @type istd: float

    @returns: The decidability value
    @rtype: float
    """
    return abs(gmean - imean) / np.sqrt(0.5 * (gstd ** 2 + istd ** 2))
