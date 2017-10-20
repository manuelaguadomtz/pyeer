# -*- coding:utf-8 -*-

import operator

import numpy as np

__copyright__ = 'Copyright 2016'
__author__ = u'Bsc. Manuel Aguado Martínez'


def calculate_eer_step_by_step(genuine_match_scores, imp_match_scores,
                               match_thr_step, hist=False):
    """Calculates the Equal Error Rate measure increasing in each step
    the matching threshold in a given value.

    Keyword Arguments:
    genuine_match_scores -- The score of each genuine match
    imp_match_scores -- The score of each impostor match
    match_thr_step -- The value in which increase the threshold at each step
    hist -- Indicates whether the impostor_match_scores came in histogram
            format. Avalaible only for integer matching thresholds step.

    :returns a tuple with the folling format: (thresholds, false match rates,
        false non match rates, EER value)
    """
    # TODO Improve the efficiency of this algorithm using numpy array from
    # the beginning for error lists

    match_thr = 0
    if hist:
        maximum_thr = max(max(genuine_match_scores), len(imp_match_scores))
    else:
        maximum_thr = max(genuine_match_scores)

    total_true_match = float(len(genuine_match_scores))
    if hist:
        total_false_match = float(sum(imp_match_scores))
        imp_match_scores = np.cumsum(imp_match_scores)
    else:
        total_false_match = float(len(imp_match_scores))

    thresholds = []
    false_match_rates = []
    false_non_match_rates = []

    while match_thr <= maximum_thr:
        if hist:
            if match_thr < len(imp_match_scores):
                false_match = total_false_match - imp_match_scores[match_thr]
            else:
                false_match = 0
        else:
            # List convertion for Python3 compatibility
            false_match = len(list(filter(lambda s: s > match_thr,
                                     imp_match_scores)))

        false_match_rates.append(false_match / total_false_match)

        # List convertion for Python3 compatibility
        false_non_match = len(list(filter(lambda s: s <= match_thr,
                                     genuine_match_scores)))
        false_non_match_rates.append(false_non_match / total_true_match)

        thresholds.append(match_thr)
        match_thr += match_thr_step

    false_match_rates = np.array(false_match_rates)
    false_non_match_rates = np.array(false_non_match_rates)
    index = np.argmin(abs(false_match_rates - false_non_match_rates))
    eer = abs(false_non_match_rates[index] + false_match_rates[index]) / 2.0

    return thresholds, false_match_rates, false_non_match_rates, eer


def calculate_eer(genuine_match_scores, impostor_match_scores):
    """Calculates the Equal Error Rate measure

    Keyword Arguments:
    genuine_match_scores -- The score of each genuine match
    impostor_match_scores -- The score of each impostor match

    :returns a tuple with the folling format: (thresholds, false match rates,
        false non match rates, EER value)
    """
    total_true_match = len(genuine_match_scores)
    total_false_match = len(impostor_match_scores)
    total = total_true_match + total_false_match

    genuine_match_scores = zip(genuine_match_scores, [1] * total_true_match)    
    genuine_match_scores = list(genuine_match_scores) # Python3 compatibility

    impostor_match_scores = zip(impostor_match_scores, [0] * total_false_match)    
    impostor_match_scores = list(impostor_match_scores) # Python3 compatibility

    scores = np.array(sorted(genuine_match_scores + impostor_match_scores,
                             key=operator.itemgetter(0)))
    sum_true = np.cumsum(scores[:, 1])
    sum_false = total_false_match - (np.arange(0, total) - sum_true)

    false_match_rates = np.ones(total + 1)
    false_non_match_rates = np.zeros(total + 1)

    false_non_match_rates[1:] = sum_true / total_true_match
    false_match_rates[1:] = sum_false / total_false_match

    thresholds = np.zeros((total + 1))
    thresholds[1:] = scores[:, 0]

    index = np.argmin(abs(false_match_rates - false_non_match_rates))
    eer = abs(false_non_match_rates[index] + false_match_rates[index]) / 2.0

    return thresholds, false_match_rates, false_non_match_rates, eer

