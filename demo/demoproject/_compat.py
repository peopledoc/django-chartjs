# -*- coding: utf-8 -*-
import sys

PY2 = sys.version_info[0] == 2


def decode(string):
    """Wrapper around 'print' for Py2/3 _compatibility."""
    if not PY2:
        return string.decode('utf-8')
    return string
