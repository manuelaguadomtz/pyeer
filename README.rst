PyEER
=====

**PyEER** is a python package for biometric systems performance evaluation. Includes ROC, DET, FNMR and FMR curves
plotting, scores distribution plotting, EER and operating points estimation. It can be also used to evaluate binary
classification systems.

Installing
----------

.. code:: sh

    pip install pyeer

Input file formats
------------------

On this epigraph the two different input file formats supported will be described.

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

**Recommendations:** Use this format for very large experiments.

**Note:** Only impostor scores file can mimic this format.

####Non-Histogram format

**Restrictions:** None. Integer and float scores are both supported.

**File format:** All the scores one by line

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
