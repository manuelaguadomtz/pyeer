# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.md') as f:
    readme = f.read()

setup(
    # Package name
    name='pyeer',

    # Package version
    version='0.5.6',

    entry_points={
        'console_scripts': [
            'geteerinf = pyeer.eer_info:get_eer_info_cmd',
            'getcmcinf = pyeer.cmc_info:get_cmc_info',
        ],
    },

    include_package_data=True,

    package_data={
        'pyeer': ['example_files/hist/*.txt', 'example_files/non_hist/*.txt',
                  'example_files/cmc/*.txt'],
    },

    # Included packages
    packages=find_packages(),

    # Package author information
    author=u'Manuel Aguado Martínez',

    author_email='manuelaguadomtz@gmail.com',

    url='https://github.com/manuelaguadomtz/pyeer',

    # project_urls={
    #     'Project Information': 'https://www.researchgate.net/project/'
    #                            'Python-package-to-calculate-EER-values'
    #                             '-and-probability-curves',
    #     'Source Code': 'https://github.com/manuelaguadomtz/pyeer',
    # },

    # Package requirements
    install_requires=['numpy',
                      'matplotlib'],

    # Package description
    description='A python package for biometric and binary classification '
                'systems performance evaluation',

    long_description=readme,

    long_description_content_type='text/markdown',

    keywords=['Equal Error Rate', 'False Match Rate', 'ROC', 'DET',
              'False Non-Match Rate', 'EER', 'FMR', 'FNMR', 'ZeroFNMR',
              'ZeroFMR', 'CMC', 'Biometric Systems'],

    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ],
)
