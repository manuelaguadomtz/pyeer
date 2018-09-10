# -*- coding:utf-8 -*-

import csv
import pkg_resources

__copyright__ = 'Copyright 2017'
__author__ = u'Bsc. Manuel Aguado Martínez'


def generate_html_eer_report(stats, ids, save_file):
    """ Generate an HTML file with the given statistics

    @param stats: An iterable with instances of the named tuple Stats
    @type stats: iterable
    @param ids: An iterable with an ID (str) for each stat
    @type ids: iterable
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
        sf.write('<th>%s</th>\n' % 'GMean')
        sf.write('<th>%s</th>\n' % 'GSTD')
        sf.write('<th>%s</th>\n' % 'IMean')
        sf.write('<th>%s</th>\n' % 'ISTD')
        sf.write('<th>%s</th>\n' % "Sensitivity index (d')")
        sf.write('<th>%s</th>\n' % 'AUC')
        sf.write('<th>%s</th>\n' % 'J-Index')
        sf.write('<th>%s</th>\n' % 'J-Index Threshold')
        sf.write('<th>%s</th>\n' % 'MCC')
        sf.write('<th>%s</th>\n' % 'MCC_TH')
        sf.write('<th>%s</th>\n' % 'EERlow')
        sf.write('<th>%s</th>\n' % 'EERhigh')
        sf.write('<th>%s</th>\n' % 'EER')
        sf.write('<th>%s</th>\n' % 'ZeroFMR')
        sf.write('<th>%s</th>\n' % 'FMR1000')
        sf.write('<th>%s</th>\n' % 'FMR100')
        sf.write('<th>%s</th>\n' % 'FMR20')
        sf.write('<th>%s</th>\n' % 'FMR10')
        sf.write('<th>%s</th>\n' % 'ZeroFNMR')
        sf.write('<th>%s</th>\n' % 'EER Threshold')
        sf.write('<th>%s</th>\n' % 'ZeroFMR Threshold')
        sf.write('<th>%s</th>\n' % 'FMR1000 Threshold')
        sf.write('<th>%s</th>\n' % 'FMR100 Threshold')
        sf.write('<th>%s</th>\n' % 'FMR20 Threshold')
        sf.write('<th>%s</th>\n' % 'FMR10 Threshold')
        sf.write('<th>%s</th>\n' % 'ZeroFNMR Threshold')
        sf.write('</tr>\n')
        sf.write('</thead>\n')

        # Writing table body
        sf.write('<tbody>\n')

        for i, st in enumerate(stats):
            # Writing stats
            sf.write('<tr>\n')
            sf.write('<td>%s</td>\n' % ids[i])
            sf.write('<td>%f</td>\n' % st.gmean)
            sf.write('<td>%f</td>\n' % st.gstd)
            sf.write('<td>%f</td>\n' % st.imean)
            sf.write('<td>%f</td>\n' % st.istd)
            sf.write('<td>%f</td>\n' % st.decidability)
            sf.write('<td>%f</td>\n' % st.auc)
            sf.write('<td>%f</td>\n' % st.j_index)
            sf.write('<td>%f</td>\n' % st.j_index_th)
            sf.write('<td>%f</td>\n' % st.mccoef)
            sf.write('<td>%f</td>\n' % st.mccoef_th)
            sf.write('<td>%f</td>\n' % st.eer_low)
            sf.write('<td>%f</td>\n' % st.eer_high)
            sf.write('<td>%f</td>\n' % st.eer)
            sf.write('<td>%f</td>\n' % st.fmr0)
            sf.write('<td>%f</td>\n' % st.fmr1000)
            sf.write('<td>%f</td>\n' % st.fmr100)
            sf.write('<td>%f</td>\n' % st.fmr20)
            sf.write('<td>%f</td>\n' % st.fmr10)
            sf.write('<td>%f</td>\n' % st.fnmr0)
            sf.write('<td>%f</td>\n' % st.eer_th)
            sf.write('<td>%f</td>\n' % st.fmr0_th)
            sf.write('<td>%f</td>\n' % st.fmr1000_th)
            sf.write('<td>%f</td>\n' % st.fmr100_th)
            sf.write('<td>%f</td>\n' % st.fmr20_th)
            sf.write('<td>%f</td>\n' % st.fmr10_th)
            sf.write('<td>%f</td>\n' % st.fnmr0_th)
            sf.write('<tr>\n')

        # Closing table body
        sf.write('</tbody>\n')

        # Writing table footer
        sf.write('<tfoot>\n')

        sf.write('<tr><td colspan="27"><strong>GMean:</strong> Genuine scores'
                 ' distribution  mean</td><tr>\n')
        sf.write('<tr><td colspan="27"><strong>GSTD:</strong> Genuine scores'
                 '  distribution standard deviation</td><tr>\n')
        sf.write('<tr><td colspan="27"><strong>IMean:</strong> Impostor scores'
                 ' distribution  mean</td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>IVariance:</strong> Impostor'
                 ' scores distribution standard deviation</td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>Sensitivity index' "(d')" ':'
                 '</strong> NICE:II protocol evaluation </td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>AUC:</strong> Area under the'
                 ' ROC curve </td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>J-Index:</strong> ' "Youden's J"
                 " statistic (Youden's Index) </td></tr>\n")
        sf.write('<tr><td colspan="27"><strong>MCC:</strong> Matthews'
                 ' Correlation Coefficient </td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>EER:</strong> Equal Error Rate'
                 '</td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>EERlow, EERhigh:</strong> See'
                 ' FVC2000 protocol evaluation </td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>FMR:</strong> False Match Rate'
                 '</td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>FNMR:</strong> False Non-Match'
                 ' Rate</td></tr>\n')
        sf.write('<tr><td colspan="27"><strong>EER Threshold:</strong> '
                 ' Threshold for which EERlow and EERHigh were calculated'
                 '</td></tr>\n')

        # Closing table footer
        sf.write('<tfoot>\n')

        # Closing html table tag
        sf.write('</table>\n')

        # Writing rates html table tag
        sf.write('<table>\n')

        # Writing table caption
        pkg_version = pkg_resources.require('pyeer')[0].version
        caption = 'FMR and FNMR curves'
        sf.write('<caption><h3>%s</h3></caption>\n' % caption)

        # Writing table headers
        sf.write('<thead>\n')
        sf.write('<tr>\n')

        max_nthrs = -1
        for i, st in enumerate(stats):
            sf.write('<td>%s (FMR)</td>\n' % ids[i])
            sf.write('<td>%s (FNMR)</td>\n' % ids[i])

            nthrs = len(st.thrs)
            if nthrs > max_nthrs:
                max_nthrs = nthrs

        sf.write('</tr>\n')
        sf.write('</thead>\n')

        # Writing table body
        sf.write('<tbody>\n')

        # Writing rates
        for i in range(max_nthrs):
            sf.write('<tr>\n')
            for st in stats:
                if i < len(st.thrs):
                    sf.write('<td>%f</td>\n' % st.fmr[i])
                    sf.write('<td>%f</td>\n' % st.fnmr[i])
                else:
                    sf.write('<td></td>\n')
                    sf.write('<td></td>\n')
            sf.write('</tr>\n')

        # Closing table body
        sf.write('</tbody>\n')

        # Closing rates html table tag
        sf.write('</table>\n')

        # Closing html tag
        sf.write('</html>\n')


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

        writer.writerow([])

        # Writing rates header
        headers = []
        max_nthrs = -1
        for i, st in enumerate(stats):
            headers += [' ', ids[i] + ' (FMR)', ids[i] + ' (FNMR)']

            nthrs = len(st.thrs)
            if nthrs > max_nthrs:
                max_nthrs = nthrs
        writer.writerow(headers)

        # Writing rates
        for i in range(max_nthrs):
            row = []
            for st in stats:
                if i < len(st.thrs):
                    row += [' ', st.fmr[i], st.fnmr[i]]
                else:
                    row += [' ', ' ', ' ']
            writer.writerow(row)


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
        generate_html_eer_report(stats, ids, save_file)
    else:
        raise ValueError('Unsupported file format')


def generate_csv_cmc_report(stats, max_rank, save_file):
    """ Generate a CSV file with the given CMC rank values

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
    """ Generate a CSV file with the given CMC rank values

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


def generate_tex_cmc_report(stats, max_rank, save_file):
    """ Generate a CSV file with the given CMC rank values

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
        sf.write('\\author{PyEER}\n')

        # Writing document begin
        sf.write('\\begin{document}\n')

        # Making title
        sf.write('\maketitle\n')

        # Beginning table
        sf.write('\\begin{table}[h]\n')

        # Centering
        sf.write('\centering')

        # Writing table caption
        pkg_version = pkg_resources.require('pyeer')[0].version
        caption = 'Generated using PyEER ' + pkg_version
        sf.write('\caption{%s.}\label{cmc_table}\n' % caption)

        # Beginning tabular block
        sf.write('\\begin{tabular}{%s}\n' % ('l' * (len(stats) + 1)))

        # Inserting line
        sf.write('\hline\n')

        # Inserting table headers
        sf.write('\\textbf{%s} ' % 'Ranks')
        for st in stats:
            sf.write(' & \\textbf{%s}' % st.exp_id)
        sf.write('\\\\\n')

        for i in range(1, max_rank + 1):
            # Writing rank values
            sf.write('\hline\n')
            sf.write('Rank-%d' % i)
            for st in stats:
                sf.write(' & %f' % st.ranks[i - 1])
            sf.write('\\\\\n')

        # Ending tabular block
        sf.write('\end{tabular}\n')

        # Ending table
        sf.write('\end{table}\n')

        # Writing document end
        sf.write('\end{document}\n')


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
    else:
        raise ValueError('Unsupported file format')
