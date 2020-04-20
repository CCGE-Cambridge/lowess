import os
import re
from setuptools import setup

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
ROOT = os.path.abspath(os.path.dirname(__file__))


def find_version(fname):
    '''
    Parse file & return version number matching v0.0.1 regex
    Returns str or raises RuntimeError
    '''
    version = ''
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    if os.path.exists(fname):
        with open(fname, 'r', encoding="utf-8") as fp:
            for line in fp:
                m = reg.match(line)
                if m:
                    version = m.group(1)
                    break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


setup(
    name='lowess',
    version=find_version(os.path.join(ROOT, 'lowess/lowess.py')),
    packages=['lowess'],
    package_data={},
    author='Andrew Lee',
    include_package_data=True,
    zip_safe=False,
    url='http://github.com/CCGE-Cambridge/lowess',
    description="Lowess smoothed as defined for STATA 13.",
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    install_requires=["pandas>=1.0.3"],
    classifiers=[
        'Intended Audience :: Scientists',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
