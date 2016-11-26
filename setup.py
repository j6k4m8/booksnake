import os
from distutils.core import setup

"""
git tag {VERSION}
git push --tags
python setup.py sdist upload -r pypi
"""

VERSION = "0.1.1"

# https://pythonhosted.org/an_example_pypi_project/setuptools.html
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "booksnake",
    version = VERSION,
    author = "Jordan Matelsky",
    author_email = "j6k4m8@gmail.com",
    description = ("Download books from the internet and send to kindle"),
    license = "BSD",
    keywords = [
        "kindle",
        "ebook",
        "download"
    ],
    url = "https://github.com/j6k4m8/booksnake/tarball/" + VERSION,
    packages=['booksnake'],
    long_description = read('README.md'),
    scripts = [
        'scripts/booksnake'
    ],
    classifiers=[],
    install_requires=[
        'BeautifulSoup'
    ],
)
