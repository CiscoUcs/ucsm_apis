#!/usr/bin/env python
# From https://github.com/pre-commit/pre-commit-hooks
# License: MIT

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

from util import added_files
from util import exists
from util import cmd_output
from util import CalledProcessError


MAX_LINE_LENGHT = 120


def check_flake8(argv=None):
    has_flake8 = exists('flake8')
    if not has_flake8:
        print('run pip install flake8')
        sys.exit(1)

    files = added_files()

    retval = 0
    for filename in files:
        try:
            out, err, rc = cmd_output('flake8', '%s' % filename)
        except CalledProcessError as e:
            retval = 1
            print("***** flake8 check failed *****")
            print(e[3])

        if retval != 0:
            sys.exit(retval)

    return retval


if __name__ == '__main__':
    exit(check_flake8())
