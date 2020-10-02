import os
from setuptools import setup, find_packages

import booksnake
from booksnake.version import __version__

VERSION = __version__

setup(
    name="booksnake",
    version=VERSION,
    author="Jordan Matelsky",
    author_email="j6k4m8@gmail.com",
    description=("Download books from the internet and send to kindle"),
    license="Apache 2.0",
    keywords=[
        "kindle",
        "ebook",
        "download"
    ],
    url="https://github.com/j6k4m8/booksnake/tarball/" + VERSION,
    packages=find_packages(exclude=["docs", "tests*"]),
    scripts=[
        'scripts/booksnake'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        'beautifulsoup4',
        'libgen-api'
    ],
)
