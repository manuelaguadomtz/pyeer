# -*- coding:utf-8 -*-

import operator

from collections import namedtuple
from warnings import warn

__copyright__ = 'Copyright 2017'
__author__ = u'Manuel Aguado Martínez'

TEMPLATE_POS = 0
SCORE_POS = 1


CMCstats = namedtuple('CMCstats', ['exp_id',  # Exp id
                                   'ranks',  # Rank values
                                   ])


def load_scores_from_file(scores_filename, true_pairs_filename,
                          ds_scores=False, delimiter=' '):
    """Loads the match information from the files.

    @param scores_filename: The scores file address. One score per
        line with the following format: (query template score)
    @type scores_filename: str
    @param true_pairs_filename: The true pairs file address. Each line
        indicates the corresponding template of each query. Must have
        the following format: (query true_template)
    @type true_pairs_filename: str
    @param ds_scores: Indicates whether te input scores are dissimilarity
        scores.
    @type ds_scores: bool
    @param delimiter: The boundary string of input files.
    @type delimiter: str, default ' '

    @returns: A dictionary {key=query, value=QueryMatchInfo}
    @rtype: dict
    """
    matching_scores = {}

    with open(true_pairs_filename) as tpf:
        for line in tpf:
            query, template = line.split(delimiter, 1)
            matching_scores[query] = (template, [])

    with open(scores_filename) as sf:
        for line in sf:
            query, template, score = line.split(delimiter)[:3]
            matching_scores[query][SCORE_POS].append((template, float(score)))

    for query_match_info in matching_scores.values():
        query_match_info[SCORE_POS].sort(key=operator.itemgetter(SCORE_POS),
                                         reverse=not ds_scores)

    return matching_scores


def get_cmc_curve(scores, max_rank):
    """Calculates the values of a CMC curve

    @param scores: The dictionary returned by the function
        load_scores_from_file or a similar one.
    @type scores: dict
    @param max_rank: The maximum rank to calculate the penetration coefficient.
    @type max_rank : int

    @return: A list with the rank values.
    @rtype: list
    """
    ranks_values = [0.0] * (max_rank + 1)
    queries_total = len(scores)

    for r in range(max_rank):
        in_rank = 0.0
        for query_match_info in scores.values():
            match = query_match_info[SCORE_POS][r]
            true_template = query_match_info[TEMPLATE_POS].strip()
            if match[TEMPLATE_POS] == true_template:
                in_rank += 1
        ranks_values[r + 1] = in_rank / queries_total + ranks_values[r]

    if ranks_values[-1] < 0.2:
        warn("It is possible that you had set the wrong score"
             " type. Please consider reviewing if you are using"
             " dissimilarity or similarity scores")

    return ranks_values[1:]
