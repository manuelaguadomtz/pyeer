PyEER
=====

**PyEER** is a python package for biometric systems performance evaluation. Includes ROC, DET, FNMR and FMR curves
plotting, scores distribution plotting, EER and operating points estimation. It can be also used to evaluate binary
classification systems.

The program provided within this package receive two files holding genuine match scores and impostor match scores [1].
Genuine match scores are obtained by matching feature sets of the same class (same person) while impostor matching
scores are obtained by matching feature sets of different classes (different persons). Using this scores the program plots
ROC, DET, FNMR(t), FMR(t) curves and estimates Equal Error Rate Value and operating points for each system scores provided.
All computations are made following the guidelines established in ISO/IEC 19795-2 (2007).

Installing
----------

.. code:: sh

    pip install pyeer

Input file formats
------------------
Genuine match scores must be provided in a file with one score per line. Each line can have any number of columns but
the score must be in the last column. For impostor match scores the program can handle two different formats:

####Histogram format

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

####Non-Histogram format

**Restrictions:** None. Integer and float scores are both supported.

**File format:** All the scores one by line, just as the genuine match scores file format

Usage
-----

**console cmd:** geteerinf

####Examples:


**To print the script help**

.. code:: sh

    geteerinf -h

**One experiment (Non-histogram format):**

.. code:: sh

    geteerinf -p "example_files/non_hist/" -i "exp1_false.txt" -g "exp1_true.txt" -e "exp1"

**More than one experiment (Non-histogram format):**

.. code:: sh

    geteerinf -p "example_files/non_hist/" -i "exp1_false.txt,exp2_false.txt" -g "exp1_true.txt,exp2_true.txt" -e "exp1,exp2"

**One experiment (Histogram format):**

.. code:: sh

    geteerinf -p "example_files/hist/" -i "exp1_false.txt" -g "exp1_true.txt" -e "exp1" -ht

**Note:** To run the above examples you can download the example files from the project site
on Gitlab or extract them from inside the package installation

Contributing
------------

Do you find **PyEER** useful? You can collaborate with us:

`Link Gitlab <https://gitlab.com/manuelaguadomtz/pyeer>`_
