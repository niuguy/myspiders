# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='streetcheck',
    version='1.0',
    packages=find_packages(),
    package_data={
        'streetcheck': ['resources/*.csv']
    },
    entry_points={'scrapy': ['settings = streetcheck.settings']},
)
