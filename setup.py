from setuptools import setup

setup(
    setup_requires=['pbr', 'pyversion'],
    pbr=True,
    auto_version="PBR",
    install_requires=open_file('requirements.txt').readlines(),
)
