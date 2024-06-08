from os import path
from setuptools import setup, find_packages

VERSION = "0.3.1"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="booksnake",
    version=VERSION,
    author="Jordan Matelsky",
    author_email="opensource@matelsky.com",
    description=("Download books from the internet and send to kindle"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    keywords=["kindle", "ebook", "download"],
    url="https://github.com/j6k4m8/booksnake/",
    packages=find_packages(exclude=["docs", "tests*"]),
    scripts=["scripts/booksnake"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["beautifulsoup4", "libgen-api", "requests"],
)
