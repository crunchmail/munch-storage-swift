#!/usr/bin/env python3
import os

from setuptools import setup
from setuptools import find_packages

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, "munch_storage_swift", "__about__.py")) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


def _find_packages(name):
    return [name] + ['{}/{}'.format(name, f) for f in find_packages(name)]

install_requires = [
    'django-storage-swift==1.2.12',
]

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    url=about["__uri__"],
    author=about["__author__"],
    author_email=about["__email__"],
    license=about["__license__"],
    packages=_find_packages('munch_storage_swift'),
    install_requires=install_requires,
    extras_require={
        'tests': [
            'bumpversion==0.5.3',
            'flake8==2.5.4']},
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',  # noqa
    ],
)
