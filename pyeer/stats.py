# -*- coding:utf-8 -*-

import operator

import numpy as np

__copyright__ = 'Copyright 2016'
__author__ = u'Bsc. Manuel Aguado Martínez'


def calculate_eer_step_by_step(gscores, iscores,
                               match_thr_step, hist=False):
    """Calculates the Equal Error Rate measure increasing in each step
    the matching threshold in a given value.

    Keyword Arguments:
    gscores -- The score of each genuine match
    iscores -- The score of each impostor match
    match_thr_step -- The value in which increase the threshold at each step
    hist -- Indicates whether the iscores came in histogram
            format. Avalaible only for integer matching thresholds step.

    :returns a tuple with the folling format: (thresholds, false match rates,
        false non match rates, EER value)
    """
    # TODO Improve the efficiency of this algorithm using numpy array from
    # the beginning for error lists

    match_thr = 0
    if hist:
        maximum_thr = max(max(gscores), len(iscores))
    else:
        maximum_thr = max(gscores)

    gscores_number = float(len(gscores))
    if hist:
        iscores_number = float(sum(iscores))
        iscores = np.cumsum(iscores)
    else:
        iscores_number = float(len(iscores))

    thresholds = []
    fm_rates = []
    fnm_rates = []

    while match_thr <= maximum_thr:
        if hist:
            if match_thr < len(iscores):
                false_match = iscores_number - iscores[match_thr]
            else:
                false_match = 0
        else:
            # List convertion for Python3 compatibility
            false_match = len(list(filter(lambda s: s > match_thr,
                                          iscores)))

        fm_rates.append(false_match / iscores_number)

        # List convertion for Python3 compatibility
        fnm = len(list(filter(lambda s: s <= match_thr, gscores)))
        fnm_rates.append(fnm / gscores_number)

        thresholds.append(match_thr)
        match_thr += match_thr_step

    fm_rates = np.array(fm_rates)
    fnm_rates = np.array(fnm_rates)
    index = np.argmin(abs(fm_rates - fnm_rates))
    eer = abs(fnm_rates[index] + fm_rates[index]) / 2.0

    return thresholds, fm_rates, fnm_rates, eer


def calculate_eer(gscores, iscores):
    """Calculates FMR, FNMR and EER

    @param gscores: Genuine matching scores
    @type gscores: list
    @param iscores: Impostor matching scores
    @type giscores: list

    @return: (thresholds, FMR, FNMR, EER)
    @rtype: tuple
    """
    gscores_number = len(gscores)
    iscores_number = len(iscores)
    scores_number = gscores_number + iscores_number

    # Labeling genuine scores as 1 and impostor scores as 0
    gscores = zip(gscores, [1] * gscores_number)
    iscores = zip(iscores, [0] * iscores_number)

    # Python3 compatibility
    gscores = list(gscores)
    iscores = list(iscores)

    # Stacking scores
    scores = np.array(sorted(gscores + iscores, key=operator.itemgetter(0)))

    # Calculating FNM and FM distributions
    fnm = np.cumsum(scores[:, 1])
    fm = iscores_number - (np.arange(0, scores_number) - fnm)

    # Calculating FMR and FNMR
    fm_rates = np.ones(scores_number + 1)
    fnm_rates = np.zeros(scores_number + 1)
    fnm_rates[1:] = fnm / gscores_number
    fm_rates[1:] = fm / iscores_number

    # Obtaining thresholds
    thresholds = np.zeros((scores_number + 1))
    thresholds[1:] = scores[:, 0]

    # Computing EER
    index = np.argmin(abs(fm_rates - fnm_rates))
    eer = abs(fnm_rates[index] + fm_rates[index]) / 2.0

    return thresholds, fm_rates, fnm_rates, eer
