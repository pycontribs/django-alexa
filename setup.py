from setuptools import setup
from os import path
from sys import version_info


def open_file(fname):
    return open(path.join(path.dirname(__file__), fname))

setup_requires = ['pbr', 'pyversion']  # TODO: unable to get pyversion working with python 3
if version_info[0] == 3:
    setup_requires = ['pbr']

setup(
    license='MIT',
    setup_requires=setup_requires,
    pbr=True,
    auto_version="PBR",
    install_requires=open(path.join(path.dirname(__file__), 'requirements.txt')).readlines(),
)
