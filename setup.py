from os import path
from setuptools import setup, find_packages

import booksnake
from booksnake.version import __version__

VERSION = __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="booksnake",
    version=VERSION,
    author="Jordan Matelsky",
    author_email="j6k4m8@gmail.com",
    description=("Download books from the internet and send to kindle"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    keywords=[
        "kindle",
        "ebook",
        "download"
    ],
    url="https://github.com/j6k4m8/booksnake/",
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
