from datetime import date
from setuptools import setup, find_packages

# python setup.py sdist
version = date.today().isoformat().replace('-', '.')

setup(
    name='cache',
    version=version,
    author='Ryan Kroon',
    author_email='rykroon.tech@gmail.com',
    packages=find_packages()
)


# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# python3 -m build
# python3 -m twine upload --repository testpypi dist/*