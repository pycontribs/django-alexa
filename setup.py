from setuptools import setup
from os import path

def open_file(fname):
    return open(path.join(path.dirname(__file__), fname))

setup(
    setup_requires=['pbr', 'pyversion'],
    pbr=True,
    auto_version="PBR",
    install_requires=open_file('requirements.txt').readlines(),
)
