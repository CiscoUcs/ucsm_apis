#!/usr/bin/env python
# From https://github.com/pre-commit/pre-commit-hooks
# License: MIT

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import ast
import platform
import sys
import traceback

from util import added_files


def check_ast(argv=None):
    files = added_files()

    retval = 0
    for filename in files:

        try:
            ast.parse(open(filename, 'rb').read(), filename=filename)
        except SyntaxError:
            print("***** ast check failed *****")
            print('{}: failed parsing with {} {}:'.format(
                filename,
                platform.python_implementation(),
                sys.version.partition(' ')[0],
            ))
            print('\n{}'.format(
                '    ' + traceback.format_exc().replace('\n', '\n    '),
            ))
            retval = 1
    return retval


if __name__ == '__main__':
    exit(check_ast())
