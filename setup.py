# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.rst') as f:
    readme = f.read()

setup(
    # Package name
    name='pyeer',

    # Package version
    version='0.4.0',

    entry_points={
        'console_scripts': [
            'geteerinf = pyeer.eer_info:get_eer_info',
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

    url='https://www.researchgate.net/profile/Manuel_Aguado_Martinez2',

    # Package requirements
    install_requires=['numpy',
                      'matplotlib'],

    # Package description
    description='A python package for biometric and binary classification '
                'systems performance evaluation',

    long_description=readme,

    keywords=['Equal Error Rate', 'False Match Rate', 'ROC', 'DET',
              'False Non-Match Rate', 'EER', 'FMR', 'FNMR', 'ZeroFNMR',
              'ZeroFMR', 'CMC', 'Biometric Systems'],
)
