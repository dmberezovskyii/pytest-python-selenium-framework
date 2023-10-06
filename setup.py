from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = [str(req) for req in parse_requirements(f)]

setup(
    name='simple framework',
    version='0.1.0',
    description='scraper',
    author='Dima Berezovskyi',
    packages=find_packages(),
    install_requires=requirements,
)
