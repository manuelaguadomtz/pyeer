# -*- coding:utf-8 -*-

import re
import os
import csv
import pkg_resources
import json
import shutil

import numpy as np

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


ROUND_DECIMAL_PLACES = 4
LATEX_TABLE_CMC_MAX_RANK = 4


def _replace_placeholder(string, placeholder, value):
    """Replaces placeholder in a file

    @param string: String with placeholders
    @param placeholder: The placeholder
    @param value: The replacement value
    """
    pattern = '{{ %s }}' % placeholder
    return re.sub(pattern, value, string)


def _get_eer_json_stats(stats, ids):
    """Get eer json stats"""

    samples = np.round(np.arange(0, 1, 0.01), 2)

    json_stats = [
        {
            'experiment': ids[i],
            'samples': samples.tolist(),
            'fnmr_samples': np.interp(
                samples, st.fmr[::-1], st.fnmr[::-1]).tolist(),
            'tpr_samples': np.interp(
                samples, st.fmr[::-1], 1 - st.fnmr[::-1]).tolist(),
            'gmean': round(st.gmean, ROUND_DECIMAL_PLACES),
            'gstd': round(st.gstd, ROUND_DECIMAL_PLACES),
            'imean': round(st.imean, ROUND_DECIMAL_PLACES),
            'istd': round(st.istd, ROUND_DECIMAL_PLACES),
            'sindex': round(st.decidability, ROUND_DECIMAL_PLACES),
            'AUC': round(st.auc, ROUND_DECIMAL_PLACES),
            'jndex': round(st.j_index, ROUND_DECIMAL_PLACES),
            'jindexTh': st.j_index_th,
            'MCC': round(st.mccoef, ROUND_DECIMAL_PLACES),
            'MCCTh': st.mccoef_th,
            'EERLow': round(st.eer_low, ROUND_DECIMAL_PLACES),
            'EERHigh': round(st.eer_high, ROUND_DECIMAL_PLACES),
            'EER': round(st.eer, ROUND_DECIMAL_PLACES),
            'ZeroFMR': round(st.fmr0, ROUND_DECIMAL_PLACES),
            'FMR1000': round(st.fmr1000, ROUND_DECIMAL_PLACES),
            'FMR100': round(st.fmr100, ROUND_DECIMAL_PLACES),
            'FMR20': round(st.fmr20, ROUND_DECIMAL_PLACES),
            'FMR10': round(st.fmr10, ROUND_DECIMAL_PLACES),
            'ZeroFNMR': round(st.fnmr0, ROUND_DECIMAL_PLACES),
            'EERTh': st.eer_th,
            'ZeroFMRTh': st.fmr0_th,
            'FMR1000Th': st.fmr1000_th,
            'FMR100Th': st.fmr100_th,
            'FMR20Th': st.fmr20_th,
            'FMR10Th': st.fmr10_th,
            'ZeroFNMRTh': st.fnmr0_th,
        }
        for i, st in enumerate(stats)
    ]

    return json.dumps(json_stats)


def generate_html_eer_report(stats, ids, save_dir):
    """ Generate an HTML file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    pkg_version = pkg_resources.require('pyeer')[0].version
    htmlpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")
    output_path = os.path.join(save_dir, "pyeer_report")

    # Copying base template
    shutil.copytree(htmlpath, output_path)

    indexbase = os.path.join(htmlpath, 'index.html')
    indexoutput = os.path.join(output_path, 'index.html')

    # Building index.html
    with open(indexbase) as fi, open(indexoutput, 'w') as fo:
        indexhtml = fi.read()

        # Replacing version
        indexhtml = _replace_placeholder(indexhtml, 'version', pkg_version)

        fo.write(indexhtml)

    # Copying data
    datafolder = os.path.join(output_path, "data")
    with open(os.path.join(datafolder, 'stats.js'), 'w') as fo:
        json_stats = _get_eer_json_stats(stats, ids)
        fo.write(f'var data = {json_stats};')


def generate_json_eer_report(stats, ids, save_file):
    """ Generate a JSON file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:
        pkg_version = pkg_resources.require('pyeer')[0].version

        jdict = {
            'Information': 'Generated using PyEER ' + pkg_version,
            'Legend:': {
                'GMean': 'Genuine scores distribution mean',
                'GSTD': 'Genuine scores distribution '
                        'standard deviation',
                'IMean': 'Impostor scores distribution mean',
                'IVariance': 'Impostor scores distribution '
                             'standard deviation',
                "Sensitivity index (d')": "See NICE:II protocol"
                                          " evaluation",
                'AUC': 'Area under the ROC curve',
                "J-Index": "Youden's J statistic (Youden's Index)",
                "MCC": "Matthews Correlation Coefficient",
                'EER': 'Equal Error Rate',
                'EERlow, EERhigh': 'See FVC2000 protocol evaluation',
                'FMR': 'False Match Rate',
                'FNMR': 'False Non-Match Rate',
                '_TH': 'Threshold',
                'EER_TH': 'Threshold for which EERlow and EERHigh were'
                          ' calculated'
            }
        }

        for i, st in enumerate(stats):
            st_dict = {
                'GMean': st.gmean,
                'GSTD': st.gstd,
                'IMean': st.imean,
                'ISTD': st.istd,
                "Sensitivity index (d')": st.decidability,
                'AUC': st.auc,
                'J-Index': st.j_index,
                'J-Index Threshold': st.j_index_th,
                'MCC': st.mccoef,
                'MCC Threshold': st.mccoef_th,
                'EERlow': st.eer_low,
                'EERhigh': st.eer_high,
                'EER': st.eer,
                'ZeroFMR': st.fmr0,
                'FMR1000': st.fmr1000,
                'FMR100': st.fmr100,
                'FMR20': st.fmr20,
                'FMR10': st.fmr10,
                'ZeroFNMR': st.fnmr0,
                'EER Threshold': st.eer_th,
                'ZeroFMR Threshold': st.fmr0_th,
                'FMR1000 Threshold': st.fmr1000_th,
                'FMR100 Threshold': st.fmr100_th,
                'FMR20 Threshold': st.fmr20_th,
                'FMR10 Threshold': st.fmr10_th,
                'ZeroFNMR Threshold': st.fnmr0_th,
            }
            jdict['Stats for %s' % ids[i]] = st_dict

        json.dump(jdict, sf, ensure_ascii=False, indent=4)


def generate_tex_eer_report(stats, ids, save_file):
    """ Generate an TEX file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # document type
        sf.write('\documentclass[10pt]{article}\n')

        # Writing document title
        sf.write('\\title{EER report}\n')

        # Writing author
        pkg_version = pkg_resources.require('pyeer')[0].version
        caption = 'Generated using PyEER ' + pkg_version
        sf.write('\\author{%s}\n' % caption)

        # Writing document begin
        sf.write('\\begin{document}\n')

        # Making title
        sf.write('\maketitle\n')

        # Table legend
        sf.write('\\begin{itemize}\n')
        sf.write('\item \\textbf{GMean:} Genuine scores distribution  mean\n')
        sf.write('\item \\textbf{GSTD:} Genuine scores distribution standard '
                 'deviation\n')
        sf.write('\item \\textbf{IMean:} Impostor scores distribution  mean\n')
        sf.write('\item \\textbf{IVariance:} Impostor scores distribution'
                 ' standard deviation')
        sf.write("\item \\textbf{Sensitivity index (d')}:NICE:II protocol "
                 "evaluation\n")
        sf.write('\item \\textbf{AUC:} Area under the ROC curve\n')
        sf.write("\item \\textbf{J-Index:} Youden's J statistic (Youden's "
                 "Index)\n")
        sf.write('\item \\textbf{MCC:} Matthews Correlation Coefficient\n')
        sf.write('\item \\textbf{EER:} Equal Error Rate\n')
        sf.write('\item \\textbf{EERlow,} EERhigh: See FVC2000 protocol '
                 'evaluation\n')
        sf.write('\item \\textbf{FMR:} False Match Rate\n')
        sf.write('\item \\textbf{FNMR:} False Non-Match Rate\n')
        sf.write('\item \\textbf{EER TH:} Threshold for which EERlow'
                 ' and EERHigh were calculated\n')
        sf.write('\item TH: Threshold\n')
        sf.write('\end{itemize}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table1}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 6))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'GMean')
        sf.write('& \\textbf{%s} ' % 'GSTD')
        sf.write('& \\textbf{%s} ' % 'IMean')
        sf.write('& \\textbf{%s} ' % 'ISTD')
        sf.write('& \\textbf{%s} ' % "d'")
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.gmean)
            sf.write(' & %f' % st.gstd)
            sf.write(' & %f' % st.imean)
            sf.write(' & %f' % st.istd)
            sf.write(' & %f' % st.decidability)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table2}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 5))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'J-Index')
        sf.write('& \\textbf{%s} ' % 'J-Index TH')
        sf.write('& \\textbf{%s} ' % 'MCC')
        sf.write('& \\textbf{%s} ' % 'MCC TH')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.j_index)
            sf.write(' & %f' % st.j_index_th)
            sf.write(' & %f' % st.mccoef)
            sf.write(' & %f' % st.mccoef_th)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table3}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 5))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'AUC')
        sf.write('& \\textbf{%s} ' % 'EERlow')
        sf.write('& \\textbf{%s} ' % 'EERhigh')
        sf.write('& \\textbf{%s} ' % 'EER')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.auc)
            sf.write(' & %f' % st.eer_low)
            sf.write(' & %f' % st.eer_high)
            sf.write(' & %f' % st.eer)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table4}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 5))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'ZeroFMR')
        sf.write('& \\textbf{%s} ' % 'FMR1000')
        sf.write('& \\textbf{%s} ' % 'FMR100')
        sf.write('& \\textbf{%s} ' % 'FMR20')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.fmr0)
            sf.write(' & %f' % st.fmr1000)
            sf.write(' & %f' % st.fmr100)
            sf.write(' & %f' % st.fmr20)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table5}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 4))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'FMR10')
        sf.write('& \\textbf{%s} ' % 'ZeroFNMR')
        sf.write('& \\textbf{%s} ' % 'EER TH')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.fmr10)
            sf.write(' & %f' % st.fnmr0)
            sf.write(' & %f' % st.eer_th)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table6}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 4))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'ZeroFMR TH')
        sf.write('& \\textbf{%s} ' % 'FMR1000 TH')
        sf.write('& \\textbf{%s} ' % 'FMR100 TH')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.fmr0_th)
            sf.write(' & %f' % st.fmr1000_th)
            sf.write(' & %f' % st.fmr100_th)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Beginning table
        sf.write('\\begin{table}\n')

        # Centering
        sf.write('\centering\n')

        # Writing table caption
        sf.write('\caption{%s.}\label{eer_table7}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * 4))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Experiment ID')
        sf.write('& \\textbf{%s} ' % 'FMR20 TH')
        sf.write('& \\textbf{%s} ' % 'FMR10 TH')
        sf.write('& \\textbf{%s} ' % 'ZeroFNMR TH')
        sf.write('\\\\\n')

        for i, st in enumerate(stats):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('%s' % ids[i])
            sf.write(' & %f' % st.fmr20_th)
            sf.write(' & %f' % st.fmr10_th)
            sf.write(' & %f' % st.fnmr0_th)
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Writing document end
        sf.write('\end{document}\n')


def generate_csv_eer_report(stats, ids, save_file):
    """ Generate a CSV file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Writing headers
        writer = csv.writer(sf)

        # Writing package version
        pkg_version = pkg_resources.require('pyeer')[0].version
        writer.writerow(['Generated using PyEER ' + pkg_version])

        row = ['Experiment ID', 'GMean', 'GSTD', 'IMean',
               'ISTD', "Sensitivity index (d')", 'AUC', 'J-Index',
               'J-Index_TH', 'MCC', 'MCC_TH', 'EERlow',
               'EERhigh', 'EER', 'ZeroFMR', 'FMR1000', 'FMR100',
               'FMR20', 'FMR10', 'ZeroFNMR', 'EER_TH', 'ZeroFMR_TH',
               'FMR1000_TH', 'FMR100_TH', 'FMR20_TH', 'FMR10_TH',
               'ZeroFNMR_TH']
        writer.writerow(row)

        for i, st in enumerate(stats):
            # Writing stats
            row = [ids[i], st.gmean, st.gstd, st.imean, st.istd,
                   st.decidability, st.auc, st.j_index, st.j_index_th,
                   st.mccoef, st.mccoef_th, st.eer_low, st.eer_high,
                   st.eer, st.fmr0, st.fmr1000, st.fmr100, st.fmr20,
                   st.fmr10, st.fnmr0, st.eer_th, st.fmr0_th, st.fmr1000_th,
                   st.fmr100_th, st.fmr20_th, st.fmr10_th, st.fnmr0_th]
            writer.writerow(row)

        # Writing legend
        writer.writerow([])
        writer.writerow(['Legend:'])
        writer.writerow(['GMean: Genuine scores distribution mean'])
        writer.writerow(['GSTD: Genuine scores distribution '
                         'standard deviation'])
        writer.writerow(['IMean: Impostor scores distribution mean'])
        writer.writerow(['IVariance: Impostor scores distribution '
                         'standard deviation'])
        writer.writerow(["Sensitivity index (d'): See NICE:II protocol"
                         " evaluation"])
        writer.writerow(['AUC: Area under the ROC curve'])
        writer.writerow(["J-Index: Youden's J statistic (Youden's Index)"])
        writer.writerow(["MCC: Matthews Correlation Coefficient"])
        writer.writerow(['EER: Equal Error Rate'])
        writer.writerow(['EERlow, EERhigh: See FVC2000 protocol evaluation'])
        writer.writerow(['FMR: False Match Rate'])
        writer.writerow(['FNMR: False Non-Match Rate'])
        writer.writerow(['_TH: Threshold'])
        writer.writerow(['EER_TH: Threshold for which EERlow and EERHigh were'
                         ' calculated'])


def export_error_rates(fmr, fnmr, filename):
    """Exports the given error rates to a CSV file

    @param fmr: False Match Rates
    @type fmr: iterable
    @param fnmr: False Non-Match Rates
    @type fnmr: iterable
    @param filename: The output filename
    @type filename: str
    """
    with open(filename, 'w') as sf:
        # Creating CSV writer
        writer = csv.writer(sf)

        # Writing rates header
        writer.writerow(['FMR', 'FNMR'])

        # Writing rates
        for i in range(len(fmr)):
            writer.writerow([fmr[i], fnmr[i]])


def generate_eer_report(stats, ids, save_file):
    """Writes EER statistics to a file

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
    @param save_file: The filename used to save the report.
        The file format will depend on the filename extension.
    @type save_file: str
    """

    # Getting file extension
    ext = save_file.split('.')[-1]

    if ext.lower() == 'csv':
        generate_csv_eer_report(stats, ids, save_file)
    elif ext.lower() == 'html':
        save_dir = os.path.dirname(save_file)
        generate_html_eer_report(stats, ids, save_dir)
    elif ext.lower() == 'tex':
        generate_tex_eer_report(stats, ids, save_file)
    elif ext.lower() == 'json':
        generate_json_eer_report(stats, ids, save_file)
    else:
        raise ValueError('Unsupported file format')


def generate_csv_cmc_report(stats, max_rank, save_file):
    """ Generates a CSV file with the given CMC rank values

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Writing headers
        writer = csv.writer(sf)
        row = ['Rank-' + str(i) for i in range(1, max_rank + 1)]
        writer.writerow(['Experiment ID'] + row)

        for st in stats:
            # Writing rank values
            writer.writerow([st.exp_id] + st.ranks)


def generate_html_cmc_report(stats, max_rank, save_file):
    """ Generates an HTML file with the given CMC rank values

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # Write html tag
        sf.write('<html>\n')

        # Writing encoding type
        sf.write('<meta charset="UTF-8">\n')

        # Writing styles
        sf.write('<style>')
        sf.write('td{ padding-right: 15px; padding-left:15px;}')
        sf.write('</style>')

        # Writing html table tag
        sf.write('<table>\n')

        # Writing table caption
        pkg_version = pkg_resources.require('pyeer')[0].version
        caption = 'Generated using PyEER ' + pkg_version
        sf.write('<caption><h3>%s</h3></caption>\n' % caption)

        # Writing table headers
        sf.write('<thead>\n')
        sf.write('<tr>\n')
        sf.write('<th>%s</th>\n' % 'Experiment ID')
        for i in range(1, max_rank + 1):
            sf.write('<th>Rank-%d</th>\n' % i)
        sf.write('</tr>\n')
        sf.write('</thead>\n')

        # Writing table body
        sf.write('<tbody>\n')

        for st in stats:
            # Writing rank values
            sf.write('<tr>\n')
            sf.write('<td>%s</td>\n' % st.exp_id)
            for r in st.ranks:
                sf.write('<td>%f</td>\n' % r)
            sf.write('</tr>\n')

        # Closing table body
        sf.write('</tbody>\n')

        # Closing html table tag
        sf.write('</table>\n')

        # Closing html tag
        sf.write('</html>\n')


def __write_cmc_tex_table(sf, table_number, stats, max_rank):
    # Beginning table
    sf.write('\\begin{table}[h]\n')

    # Centering
    sf.write('\centering')

    # Writing table caption
    label = 'cmc_table' + str(table_number + 1)
    sf.write('\caption{CMC Ranks.}\label{%s}\n' % label)

    # Beginning tabular block
    sf.write('\\begin{tabular}{%s}\n' % ('l' * (LATEX_TABLE_CMC_MAX_RANK + 1)))

    # Inserting line
    sf.write('\hline\n')

    rstart = table_number * LATEX_TABLE_CMC_MAX_RANK
    rend = rstart + LATEX_TABLE_CMC_MAX_RANK

    # Inserting table headers
    sf.write('\\textbf{%s} ' % 'Experiment ID')
    for i in range(rstart + 1, min(max_rank, rend) + 1):
        sf.write(' & \\textbf{Rank-%d}' % i)
    sf.write('\\\\\n')

    for st in stats:
        # Writing rank values
        sf.write('\hline\n')
        sf.write('%s' % st.exp_id)
        for i in range(rstart, min(max_rank, rend)):
            sf.write(' & %f' % st.ranks[i])
        sf.write('\\\\\n')

    # Ending tabular block
    sf.write('\end{tabular}\n')

    # Ending table
    sf.write('\end{table}\n')


def generate_tex_cmc_report(stats, max_rank, save_file):
    """ Generates a TEX file with the given CMC rank values

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:

        # document type
        sf.write('\documentclass[10pt]{article}\n')

        # Writing document title
        sf.write('\\title{CMC report}\n')

        # Writing author
        pkg_version = pkg_resources.require('pyeer')[0].version
        caption = 'Generated using PyEER ' + pkg_version
        sf.write('\\author{%s}\n' % caption)

        # Writing document begin
        sf.write('\\begin{document}\n')

        # Making title
        sf.write('\maketitle\n')

        table_count = int(max_rank / LATEX_TABLE_CMC_MAX_RANK)
        if max_rank % LATEX_TABLE_CMC_MAX_RANK != 0:
            table_count += 1
        for i in range(table_count):
            __write_cmc_tex_table(sf, i, stats, max_rank)

        # Writing document end
        sf.write('\end{document}\n')


def generate_json_cmc_report(stats, max_rank, save_file):
    """ Generates a JSON file with the given CMC rank values

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report
    @type save_file: str
    """
    with open(save_file, 'w') as sf:
        pkg_version = pkg_resources.require('pyeer')[0].version

        jdict = {
            'Information': 'Generated using PyEER ' + pkg_version,
        }

        for st in stats:
            jdict['Rank values for %s' % st.exp_id] = st.ranks

        json.dump(jdict, sf, ensure_ascii=False, indent=4)


def generate_cmc_report(stats, max_rank, save_file):
    """ Writes CMC rank values to a file

    @param exps_cmc: A list of CMCstats instances
    @type exps_cmc: list
    @param max_rank: The maximum rank of the CMC curves
    @type max_rank: int
    @param save_file: The filename used to save the report.
        The file format will depend on the filename extension.
    @type save_file: str
    """
    # Getting file extension
    ext = save_file.split('.')[-1]

    if ext.lower() == 'csv':
        generate_csv_cmc_report(stats, max_rank, save_file)
    elif ext.lower() == 'html':
        generate_html_cmc_report(stats, max_rank, save_file)
    elif ext.lower() == 'tex':
        generate_tex_cmc_report(stats, max_rank, save_file)
    elif ext.lower() == 'json':
        generate_json_cmc_report(stats, max_rank, save_file)
    else:
        raise ValueError('Unsupported file format')
