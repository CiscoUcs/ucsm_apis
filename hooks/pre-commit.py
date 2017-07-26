#!/usr/bin/env python

import sys

from check_ast import check_ast
from check_flake8 import check_flake8
from check_merge_conflict import detect_merge_conflict

def main(argv=None):
    rc = 0
    try:
        check_flake8()
    except:
        rc = 1

    try:
        check_ast()
    except:
        rc = 1

    try:
        detect_merge_conflict()
    except:
        rc = 1

    return rc


if __name__ == '__main__':
    exit(main())



