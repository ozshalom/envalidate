"""Setup."""

import os

from envalidate import VERSION
from setuptools import find_packages, setup

folder = os.path.dirname(__file__)
with open(os.path.join(folder, 'README.md')) as f:
    readme = f.read()

with open(os.path.join(folder, 'LICENSE')) as f:
    license_txt = f.read()

with open(os.path.join(folder, 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='envalidate',
    version=VERSION,
    description='validating and accessing environment variables in python',
    long_description=readme,
    author='oz shalom',
    author_email='oz.shalom0175@gmaill.com',
    url='https://github.com/ozshalom/envalidate',
    license=license_txt,
    packages=find_packages(exclude=('docs', 'tests')),
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
