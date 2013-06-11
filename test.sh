#!/bin/bash
python setup.py develop
(cd demo; python setup.py develop)
demo test demoproject
flake8 i18nurl
