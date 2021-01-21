"""
Cartoonize installation:
python setup.py install
"""
from setuptools import setup, find_packages

setup(
    name="cartoonize",
    version="1.0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
)
