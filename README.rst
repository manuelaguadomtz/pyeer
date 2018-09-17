=====
PyEER
=====

**PyEER** is a python package for biometric systems performance evaluation. Includes ROC, DET, FNMR, FMR and CMC curves
plotting, scores distribution plotting, EER and operating points estimation. It can be also used to evaluate binary
classification systems.

Two programs are provided within this package:

**geteerinf:** Receive two files holding genuine match scores and impostor match scores [1].
Genuine match scores are obtained by matching feature sets of the same class (same person), while impostor matching
scores are obtained by matching feature sets of different classes (different persons). Using these scores the program 
plots ROC, DET, FNMR(t), FMR(t) curves and estimates Equal Error Rate Value and operating points for each system. EER 
values are  reported as specified in [2]

**getcmcinf:** Receive two files holding match scores and genuine query-template pairs [1]. This program is provided to 
evaluate biometrics systems in identification scenarios. Using the scores provided, CMC curves and rank values for each 
score file are reported.

Utilities provided within this package can also be used to develop other scripts by importing the module **pyeer**.

**PyEER** has been developed with the idea of providing researchers and the scientific community in general with a 
tool to correctly evaluate and report the performance of their systems.

Installing
==========

.. code:: sh

    pip install pyeer

geteerinf input file formats
============================
Genuine match scores must be provided in a file with one score per line. Each line can have any number of columns but
the scores must be in the last column. For impostor match scores the program can handle two different formats:

Histogram format
----------------

Although the vast majority of the systems report scores normalized between 0 and 1, there are some that report
integer scores [3]. When computing a lot of impostor scores, millions of them, it can be computationally 
expensive to read all those scores from a file. Therefore, in those cases may be worth it to use this format.

**Restrictions:** Only integer scores are supported

**File format:** Each line contains the number of scores equals to the index of the line in the file
(starting from zero). For example, given a file:

| 123
| 12
| 212
| 321
| ...
| ...
| ...
|

The above file example indicates that there are 123 scores equals to 0, 12 scores equals to 1, 212 scores
equals to 2, 321 scores equals to 3 and so on.

**Recommendations:** Use this format for very large experiments (millions of scores).

**Note:** Only impostor scores file can mimic this format.

Non-Histogram format
--------------------

**Restrictions:** None. Integer and float scores are both supported.

**File format:** All the scores one by line, just as the genuine match scores file format

getcmcinf input file formats
============================

An scores file for each experiment must be provided. Also, the relation of true correspondences must be specified in
order to calculate the CMC curve.

Scores file
-----------

Each line must have the following format: (query template score)

Genuine query-template pairs
----------------------------

Each line must have the following format: (query corresponding_template)

Usage
=====

**console cmd:** geteerinf
**console cmd:** getcmcinf

Examples:
---------


**To print the script help**

.. code:: sh

    geteerinf -h

**One experiment (Non-histogram format):**

.. code:: sh

    geteerinf -p "example_files/non_hist/" -i "exp3_false.txt" -g "exp3_true.txt" -e "exp3"

**More than one experiment (Non-histogram format):**

.. code:: sh

    geteerinf -p "example_files/non_hist/" -i "exp1_false.txt,exp2_false.txt" -g "exp1_true.txt,exp2_true.txt" -e "exp1,exp2"

**One experiment (Histogram format):**

.. code:: sh

    geteerinf -p "example_files/hist/" -i "exp1_false.txt" -g "exp1_true.txt" -e "exp1" -ht

**More than one experiment (Identification experiment):**

.. code:: sh

    getcmcinf -p "example_files/cmc/" -ms "exp1_scores.txt,exp2_scores.txt" -t "exp1_tp.txt,exp2_tp.txt" -e "Exp1,Exp2"


For all the above examples a CSV file will be generated in the directory where the program was invoked. The CSV file will 
include all the calculated stats. To specify the directory where to saved it, you can use the "-sp" option.

**Note:** To run the above examples you can download the score files from the project site on Gitlab or extract them from 
inside the package installation.

**To use from other scripts**

.. code:: python

    from pyeer.eer_info import get_eer_stats
    from pyeer.report import generate_eer_report, export_error_rates
    from pyeer.plot import plot_eer_stats

    # Calculating stats for classifier A
    stats_a = get_eer_stats(gscores_a, iscores_a)

    # Calculating stats for classifier B
    stats_b = get_eer_stats(gscores_b, iscores_b)

    # Generating CSV report
    generate_eer_report([stats_a, stats_b], ['A', 'B'], 'report.csv')

    # Generating HTML report
    generate_cmc_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.html')

    # Generating Latex report
    generate_cmc_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.tex')

    # Exporting error rates
    export_error_rates(stats_a.fmr, stats_a.fnmr, 'A_DET.csv')
    export_error_rates(stats_b.fmr, stats_b.fnmr, 'B_DET.csv')

    # Plotting
    plot_eer_stats([stats_a, stats_b], ['A', 'B'])

.. code:: python

    from pyeer.cmc_stats import load_scores_from_file, get_cmc_curve, CMCstats
    from pyeer.report import generate_cmc_report
    from pyeer.plot import plot_cmc_stats

    # CMC maximum rank
    r = 20

    # Loading scores
    sfile = 'cmc/exp1_scores.txt'  # The scores file
    tp_file = 'cmc/exp1_tp.txt'  # The genuine pairs relationship in "sfile"
    scores = load_scores_from_file(sfile, tp_file)

    # Calculating CMC curve
    ranks = get_cmc_curve(scores, r)

    # Creating stats
    stats = [CMCstats(exp_id='A', ranks=ranks)]

    # Generating CSV report
    generate_cmc_report(stats, r, 'pyeer_report.csv')

    # Generating HTML report
    generate_cmc_report(stats, r, 'pyeer_report.html')

    # Generating Latex report
    generate_cmc_report(stats, r, 'pyeer_report.tex')

    # Plotting
    plot_cmc_stats(stats, r)


Contributing
============

Do you find **PyEER** useful? You can collaborate with us:

`Link GitHub <https://github.com/manuelaguadomtz/pyeer>`_

References
==========

[1] D. Maltoni et al., Handbook of Fingerprint Recognition, Springer-Verlag London Limited 2009

[2] Maio D., Maltoni D., Cappelli R., Wayman J.L. and Jain A.K., "FVC2000: Fingerprint verification
competition,"" IEEE Transactions on Pattern Analysis Machine Intelligence, vol. 24, no. 3, pp. 402–412,
2002

[3] Hernandez-Palancar, J., Munoz-Briseno, A., & Gago-Alonso, A. (2014). Using a triangular matching
approach for latent fingerprint and palmprint identification. International Journal of Pattern 
Recognition and Artificial Intelligence, 28, 1460004.