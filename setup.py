from setuptools import setup
from os import path

setup(
    name='Golem-Verificator-Experiments',
    version='0.0.1',
    url='https://github.com/magdasta/golem-verificator-experiments',
    maintainer='Magda Stasiewicz',
    maintainer_email='',
    packages=[
        'classification',
        'classification.metrics'
    ],
    package_dir={'golem_verificator_experiments': 'golem_verificator_experiments'},
    python_requires='>=3.6'
)
