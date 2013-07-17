import backdropsend
from setuptools import setup, find_packages

setup(
    name='backdropsend',
    version=backdropsend.__VERSION__,
    packages=find_packages(exclude=['test*']),
    scripts=['backdrop-send'],

    # metadata for upload to PyPI
    author=backdropsend.__AUTHOR__,
    author_email=backdropsend.__AUTHOR_EMAIL__,
    maintainer='Government Digital Service',
    url='https://github.com/alphagov/backdrop-send',

    description='backdrop-send: CLI tool for sending data to Backdrop',
    license='MIT',
    keywords='api data performance_platform',

    data_files=[('/usr/share/man/man1', ['docs/backdrop-send.1.gz'])],

    install_requires=['requests', 'argparse'],
)
