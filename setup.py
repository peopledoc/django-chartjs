# -*- coding: utf-8 -*-
import codecs
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

here = abspath(dirname(__file__))


def read_relative_file(filename):
    """Returns contents of the given file, whose path is supposed relative
    to this module."""
    with codecs.open(join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content


if __name__ == '__main__':  # ``import setup`` doesn't trigger setup().
    setup(
        name='django-chartjs',
        version=read_relative_file('VERSION').strip(),
        description="Django Chart.js and Hightchart ajax views",
        long_description=read_relative_file('README.rst'),
        classifiers=['Development Status :: 4 - Beta',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Framework :: Django :: 1.10',
                     'Framework :: Django :: 1.8',
                     'Framework :: Django :: 1.9',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5'],
        keywords='django chart chartjs highchart ajax class based views',
        author='Rémy Hubscher',
        author_email='hubscher.remy@gmail.com',
        url='https://github.com/novapost/django-chartjs',
        license='BSD Licence',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=['six']
    )
