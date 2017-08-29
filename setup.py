# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='ResParse',
    version='0.0.1',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'ResParse': ['data/*/*']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'ResParse = ResParse.cli:main',
        ],
    },
    install_requires=(
    	['nltk==3.2.1','pdfminer==20140328','wheel==0.24.0','numpy==1.11.3']
    )
)
