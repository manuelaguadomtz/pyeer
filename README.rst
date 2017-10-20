PyEER
=====

**PyEER** is a python package with utilities to calculate Equal Error Values, operation points
and to plot the probability error curves.

Installing
----------

.. code:: sh

    pip install pyeer

Input file formats
------------------

On this epigraph the two different input file formats supported will be described.

Histogram format
................

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

Non-Histogram format
....................

**Restrictions:** None. Integer and float scores are both supported.

**File format:** All the scores one by line

Usage
-----

**main script:** plot_roc_curves.py

Examples:
.........

**To print the script help**

.. code:: sh

    python plot_roc_curves.py -h

**One experiment (Non-histogram format):**

.. code:: sh

    python plot_roc_curves.py -p "example_files/non_hist/" -i "exp1_false" -g "exp1_true" -e "exp1"

**More than one experiment (Non-histogram format):**

.. code:: sh

    python plot_roc_curves.py -p "example_files/non_hist/" -i "exp1_false,exp2_false" -g "exp1_true,exp2_true" -e "exp1,exp2"

**One experiment (Histogram format):**

.. code:: sh

    python plot_roc_curves.py -p "example_files/hist/" -i "exp1_false" -g "exp1_true" -e "exp1" -ht

Contributing
------------

Do you find **PyEER** useful? You can collaborate with us:

`Link Gitlab <https://gitlab.com/manuelaguadomtz/pyeer>`_
