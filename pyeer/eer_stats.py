# -*- coding:utf-8 -*-

import operator
import warnings

from collections import namedtuple
from warnings import warn

import numpy as np


__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


Stats = namedtuple('Stats', [

    # Rate curves
    'thrs',  # Thresholds
    'fmr',  # False match rates
    'fnmr',  # False non-match rates
    'auc',  # Area under the ROC curve
    'j_index',  # Youden's index
    'j_index_th',  # Youden's index threshold
    'mccoef',  # Matthew correlation coefficient
    'mccoef_th',  # Matthew correlation coefficient threshold

    # Operation points
    'fmr0',  # Zero false math rate
    'fmr1000',  # 1000 false match rate
    'fmr100',  # 100 false match rate
    'fmr20',  # 20 false match rate
    'fmr10',  # 10 false match rate
    'fnmr0',  # 0 false non-match rate

    # Operation points thresholds
    'fmr0_th',  # Zero false math rate threshold
    'fmr1000_th',  # 1000 false match rate threshold
    'fmr100_th',  # 100 false match rate threshold
    'fmr20_th',  # 20 false match rate threshold
    'fmr10_th',  # 10 false match rate threshold
    'fnmr0_th',  # 0 false non-match rate threshold

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
    'eer_high',  # Equal error rate (high)
    'eer_th'  # The threshold for which eer_low and eer_high were calculated
])


def calculate_roc_hist(gscores, iscores, ds_scores=False, rates=True):
    """Calculates FMR, FNMR for impostor scores in histogram format

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list
    @param ds_scores: Indicates whether input scores are
        dissimilarity scores
    @type ds_scores: bool
    @param rates: Indicates whether to return error rates instead
        of error values
    @type rates: bool

    @return: (thresholds, FMR, FNMR) or (thresholds, FM, FNM)
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

        fm_rates.append(false_match)

        # List convertion for Python3 compatibility
        if ds_scores:
            fnm = len(list(filter(lambda s: s > match_thr, gscores)))
        else:
            fnm = len(list(filter(lambda s: s < match_thr, gscores)))
        fnm_rates.append(fnm)

        thresholds.append(match_thr)
        match_thr += 1

    if rates:
        fm_rates = np.array(fm_rates) / iscores_number
        fnm_rates = np.array(fnm_rates) / gscores_number
    else:
        fm_rates = np.array(fm_rates)
        fnm_rates = np.array(fnm_rates)

    return thresholds, fm_rates, fnm_rates


def calculate_roc(gscores, iscores, ds_scores=False, rates=True):
    """Calculates FMR, FNMR

    @param gscores: Genuine matching scores
    @type gscores: Union[list, ndarray]
    @param iscores: Impostor matching scores
    @type giscores: Union[list, ndarray]
    @param ds_scores: Indicates whether input scores are
        dissimilarity scores
    @type ds_scores: bool
    @param rates: Indicates whether to return error rates instead
        of error values
    @type rates: bool

    @return: (thresholds, FMR, FNMR) or (thresholds, FM, FNM)
    @rtype: tuple
    """
    if isinstance(gscores, list):
        gscores = np.array(gscores, dtype=np.float64)

    if isinstance(iscores, list):
        iscores = np.array(iscores, dtype=np.float64)

    if gscores.dtype == np.int:
        gscores = np.float64(gscores)

    if iscores.dtype == np.int:
        iscores = np.float64(iscores)

    if ds_scores:
        gscores = gscores * -1
        iscores = iscores * -1

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
    if rates:
        fnm_rates = fnm / gscores_number
        fm_rates = fm / iscores_number
    else:
        fnm_rates = fnm
        fm_rates = fm

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

    auc = ((x1 - x2) * (y1 + (y2 - y1) / 2)).sum()

    if auc < 0.5:
        warn("It is possible that you had set the wrong score"
             " type. Please consider reviewing if you are using"
             " dissimilarity or similarity scores")

    return auc


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

    @returns: Index, The lowest FMR at which the probability of FNMR == op
    @rtype: float
    """
    temp = abs(fnmr - op)
    min_val = np.min(temp)
    index = np.where(temp == min_val)[0][-1]
    return index, fmr[index]


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

    @returns: Index, The lowest FNMR at which the probability of FMR == op
    @rtype: float
    """
    index = np.argmin(abs(fmr - op))
    return index, fnmr[index]


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

    @returns: index for EERlow and EERhigh, EERlow, EERhigh, EER
    @rtype: tuple
    """
    diff = fmr - fnmr
    t2 = np.where(diff <= 0)[0]

    if len(t2) > 0:
        t2 = t2[0]
    else:
        warnings.warn('It seems that the FMR and FNMR curves'
                      ' do not intersect each other. Did you mean'
                      ' to use dissimilarity scores?', RuntimeWarning)
        return 0, 1, 1, 1

    t1 = t2 - 1 if diff[t2] != 0 and t2 != 0 else t2

    if fmr[t1] + fnmr[t1] <= fmr[t2] + fnmr[t2]:
        return t1, fnmr[t1], fmr[t1], (fnmr[t1] + fmr[t1]) / 2
    else:
        return t2, fmr[t2], fnmr[t2], (fnmr[t2] + fmr[t2]) / 2

    # index = np.argmin(abs(fmr - fnmr))
    # eer = np.abs(fnmr[index] + fmr[index]) / 2.0
    # return min(fnmr[index], fmr[index]), max(fnmr[index], fmr[index]), eer


def get_decidability_value(gmean, gstd, imean, istd):
    """ The decidability score (d') or decision-making power used in NICE:II
    evauation protocol for iris, it is a measure of the separation between
    genuine and impostor distributions. Higher d' values indicate better
    separation. It is also called the sensitivity index.

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
    if gstd == 0 and istd == 0:
        return 1
    return abs(gmean - imean) / np.sqrt(0.5 * (gstd ** 2 + istd ** 2))


def get_youden_index(fmr, fnmr):
    """Computes the Youden's index and the corresponding threshold

    Reference:
    Youden, W. J. (1950). "Index of rating diagnostic tests". Cancer. 3: 32-35

    @param fmr: False Match Rates (FMR)
    @type fmr: ndarray
    @param fnmr: False Non-Match Rates (FNMR)
    @type fnmr: ndarray

    @returns: Youden's Index, threshold
    @rtype: tuple
    """
    # J = sensitivity + specificity -1
    # sensitivity = 1 - fnmr
    # specificity = 1 - fmr
    # J = 1 - fnmr + 1 - fmr - 1
    # J = 1 - fnmr - fmr
    j = 1 - fnmr - fmr
    th = np.argmax(j)
    return j[th], th


def get_matthews_ccoef(fm, fnm, gnumber, inumber):
    """Estimate the maximum Matthews Correlation Coefficient
    given the values of false match (false positives) and false
    non-match (false negatives) for all possible thresholds

    @param fm: False Positives for all possible thresholds
    @type fm: ndarray
    @param fnm: False Negatives for all possible thresholds
    @type fnm: ndarray
    @param gnumber: The number of positive samples
    @type gnumber: int
    @param inumber: The number of negative samples
    @type inumber: int

    @returns: (Matthews Correlation Coefficient, threshold)
    @rtype: tuple
    """
    tn = inumber - fm
    tp = gnumber - fnm

    numerator = tp * tn - fm * fnm

    # Calculating sqrt for each element instead of only once to
    # all denominator to avoid overflow in some cases
    denominator_a = np.sqrt((tp + fm)) * np.sqrt((tp + fnm))
    denominator_b = np.sqrt((tn + fm)) * np.sqrt((tn + fnm))
    denominator = denominator_a * denominator_b

    denominator[denominator == 0] = 1

    all_mcc = numerator / denominator

    th = np.argmax(all_mcc)
    return all_mcc[th], th
