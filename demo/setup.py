# coding=utf-8
"""Python packaging."""
import os
from setuptools import setup


def read_relative_file(filename):
    """Returns contents of the given file, which path is supposed relative
    to this module."""
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


NAME = 'django-chartjs-demo'
README = read_relative_file('README')
VERSION = '0.1'
PACKAGES = ['demoproject']
REQUIRES = ['django-chartjs']


setup(name=NAME,
      version=VERSION,
      description='Demo project for django-chartjs.',
      long_description=README,
      classifiers=['Development Status :: 1 - Planning',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 2.6',
                   'Framework :: Django',
                   ],
      keywords='class-based view, generic view, download',
      author=u'Rémy HUBSCHER',
      author_email='remy.hubscher@novapost.fr',
      url='https://github.com/novagile/django-chartjs',
      license='BSD',
      packages=PACKAGES,
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIRES,
      entry_points={
          'console_scripts': [
              'demo = demoproject.manage:main',
          ]
      },
      )
