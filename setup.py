from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='gpcharts',
    version='1.2.1',
    description='Google Charts API wrapper',
    long_description=long_description,
    url='https://github.com/Dfenestrator/GooPyCharts',
    author='Sagnik Ghosh',
    license='Apache 2',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache 2 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=['api'],
    packages=find_packages(),
    install_requires=['future==0.16.0']
)
