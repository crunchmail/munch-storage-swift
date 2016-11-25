import os
import re

from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open('munch_storage_swift/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


def _find_packages(name):
    return [name] + ['{}/{}'.format(name, f) for f in find_packages(name)]

install_requires = [
    'django-storage-swift==1.2.12',
]

setup(
    name='munch-storage-swift',
    version=version,
    description='Swift storage backends for Munch',
    long_description=README,
    url='https://github/crunchmail/munch-storage-swift',
    author='Oasiswork',
    author_email='dev@oasiswork.fr',
    license='Proprietary License',
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
        'License :: Other/Proprietary License',
    ],
)
