import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="PiTools",
    version="1.0.0",
    author="Colton Neary",
    author_email="schneeple@outlook.com",
    description=("Pull Pi Data from Pi using PIWebAPI"),
    license="Schneeple",
    keywords="API, Pi, Python, Data Analysis Tool",
    url="https://github.com/schneeple/pitools",
    long_description=read('README.md'),
    python_requires='>=3.6',
)
