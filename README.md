# PyEER

**PyEER** is a python package intended for biometric systems performance evaluation but it can be used to evaluate binary
classification systems also. It has been developed with the idea of providing researchers and the scientific community in
general with a tool to correctly evaluate and report the performance of their systems.

Within this package, two command line programs are provided:

* **geteerinf:** Useful to evaluate biometrics systems in verification scenarios as well as binary classification systems.

* **getcmcinf:** Useful to evaluate biometrics systems in identification scenarios.

Utilities provided within this package can also be used to develop other scripts by importing the module **pyeer**.

## Installing

To install the **PyEER** package you only need to type into a terminal the following line:

    pip install pyeer

## Usage

Using **PyEER** is very easy and straightforward. Don't you believe? Let's see if we can convince you.

### geteerinf

When evaluating biometric systems in verification scenarios some researchers will only report Equal Error Rate (EER) values
to show the accuracy of their proposals. However, this is wrong. The behavior of biometric systems cannot be fully assessed in this way. In other to achieve that, Receiver Operating Characteristic (ROC) or Detection Error Tradeoff (DET) graph must
be reported. It is also very common to report other operating points besides EER (i.e. MR100, FMR1000, ZeroFMR, and ZeroFNMR).
**geteerinf** provides these and more. You will only need to provide genuine match scores and impostor match scores [1]. Genuine
match scores are obtained by matching feature sets of the same class (same person), while impostor matching scores are obtained
by matching feature sets of different classes (different persons).

#### Input file formats

Genuine match scores and impostor match scores must be provided in separated files one score per line. Each line can have any
number of columns but the scores must be in the last column. Additionally, impostor match scores can be provided in a different
format which explained next

###### Histogram format 

Although the vast majority of the systems report scores normalized between 0 and 1, there are some that
report integer scores [3]. When computing a lot of impostor scores, millions of them, it can be computationally expensive to read
all those scores from a file. Therefore, in those cases may be worth it to use this format.

Restrictions: Only integer scores are supported

File format: Each line contains the number of scores equals to the index of the line in the file (starting from zero).

Recommendations: Use this format for very large experiments (millions of scores).

If you have any doubts left, you should check the example files on [GitHub](https://github.com/manuelaguadomtz/pyeer/tree/master/pyeer/example_files).

#### Usage examples

##### To print the help

    geteerinf -h

##### One experiment (Non-histogram format):

    geteerinf -p "example_files/non_hist/" -i "exp3_false.txt" -g "exp3_true.txt" -e "exp3"

##### More than one experiment (Non-histogram format):

    geteerinf -p "example_files/non_hist/" -i "exp1_false.txt,exp2_false.txt" -g "exp1_true.txt,exp2_true.txt" -e "exp1,exp2"

##### One experiment (Histogram format):

    geteerinf -p "example_files/hist/" -i "exp1_false.txt" -g "exp1_true.txt" -e "exp1" -ht

#### Output

All of the above examples will generate the following information:

* Graphs: 
    * Receiver operating characteristic (ROC)
    * Detection error tradeoff (DET)
    * False Match Rate (FMR) and False Non-Match Rate(FNMR)
    * Genuine and impostor score histograms
* pyeer_report.csv: 
    * Genuine scores mean
    * Genuine sores standard deviation
    * Impostor scores mean
    * Impostor sores standard deviation
    * Sensitivity index (d') (See [NICE:II](http://nice2.di.ubi.pt/) protocol evaluation)
    * Equal Error Rate (EER) (EER values are reported as specified in [2]).
    * Area under the ROC curve
    * Youden's J statistic (Youden's Index)
    * Youden's Index threshold
    * Matthews Correlation Coefficient (MCC)
    * Matthews Correlation Coefficient threshold
    * Equal Error Rate (EER) (EER values are reported as specified in [2]).
    * ZeroFMR, FMR1000, FMR100, FMR20, FMR10, and ZeroFNMR
    * Equal Error Rate threshold
    * ZeroFMR, FMR1000, FMR100, FMR20, FMR10, and ZeroFNMR thresholds
* rates.csv:
    * False Match Rates
    * False Non-Match Rates

#### To use from your own scripts

    from pyeer.eer_info import get_eer_stats
    from pyeer.report import generate_eer_report, export_error_rates
    from pyeer.plot import plot_eer_stats

    # Calculating stats for classifier A
    stats_a = get_eer_stats(gscores_a, iscores_a)

    # Calculating stats for classifier B
    stats_b = get_eer_stats(gscores_b, iscores_b)

    # Generating CSV report
    generate_eer_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.csv')

    # Generating HTML report
    generate_eer_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.html')

    # Generating Latex report
    generate_eer_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.tex')

    # Generating JSON report
    generate_eer_report([stats_a, stats_b], ['A', 'B'], 'pyeer_report.json')

    # Exporting error rates (Exporting FMR and FNMR to a CSV file)
    # This is the DET curve, the ROC curve is a plot of FMR against 1 - FNMR
    export_error_rates(stats_a.fmr, stats_a.fnmr, 'A_DET.csv')
    export_error_rates(stats_b.fmr, stats_b.fnmr, 'B_DET.csv')

    # Plotting
    plot_eer_stats([stats_a, stats_b], ['A', 'B'])

### getcmcinf

In identification experiments in closed sets sometimes only rank values are reported [1]. To obtain rank values and the Cumulative match curve (CMC) **getcmcinf** is provided. It receives the match scores and genuine correspondences. The input format will be described
next.

#### Input files format

Input files must have the following formats:

* **Match scores:** Each line must have the following format: (query template score)

* **Genuine query-template pairs:** Each line must have the following format: (query corresponding_template)

For more clarification, you should check the example files on [GitHub](https://github.com/manuelaguadomtz/pyeer/tree/master/pyeer/example_files).

#### Usage examples

##### To print the script help

    getcmcinf -h

##### One experiment

    getcmcinf -p "example_files/cmc/" -ms "exp1_scores.txt" -t "exp1_tp.txt" -e "Exp1"

##### More than one experiment

    getcmcinf -p "example_files/cmc/" -ms "exp1_scores.txt,exp2_scores.txt" -t "exp1_tp.txt,exp2_tp.txt" -e "Exp1,Exp2"


#### Output

All of the above examples will generate the following information:

* Graphs: 
    * Cumulative match curve (CMC)
    
* pyeer_report.csv: 
    * Rank identification rates

#### To use from your own scripts

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

    # Generating Latex report
    generate_cmc_report(stats, r, 'pyeer_report.json')

    # Plotting
    plot_cmc_stats(stats, r)


## Contributing

Do you find **PyEER** useful? You can collaborate with us:

[GitHub](https://github.com/manuelaguadomtz/pyeer>)

Please follow our contributing guidelines.

### Contributors

We would like to thanks to those who has collaborated with the project:

* [ljsoler](https://github.com/ljsoler)
    * Added support in CMC stats for multiple templates for a single query
* [jpalancar](https://github.com/jpalancar)
    * Testing and guidance


## References

[1] D. Maltoni et al., Handbook of Fingerprint Recognition, Springer-Verlag London Limited 2009

[2] Maio D., Maltoni D., Cappelli R., Wayman J.L., and Jain A.K., "FVC2000: Fingerprint verification
competition,"" IEEE Transactions on Pattern Analysis Machine Intelligence, vol. 24, no. 3, pp. 402–412,
2002

[3] Hernandez-Palancar, J., Munoz-Briseno, A., & Gago-Alonso, A. (2014). Using a triangular matching
approach for latent fingerprint and palmprint identification. International Journal of Pattern 
Recognition and Artificial Intelligence, 28, 1460004.

