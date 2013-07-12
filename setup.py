import backdrop
from setuptools import setup, find_packages

setup(
    name='backdrop-send',
    version=backdrop.__VERSION__,
    packages=find_packages(exclude=['test*']),
    scripts=['backdrop-send'],

    # metadata for upload to PyPI
    author=backdrop.__AUTHOR__,
    author_email=backdrop.__AUTHOR_EMAIL__,
    maintainer='Government Digital Service',
    url='https://github.com/alphagov/backdrop-send',

    description='backdrop-send: CLI tool for sending data to Backdrop',
    license='MIT',
    keywords='api data performance_platform',

    install_requires=['requests', 'argparse'],
)
