#!/usr/bin/env python
# From https://github.com/pre-commit/pre-commit-hooks
# License: MIT

from __future__ import print_function

import os.path

from util import added_files

CONFLICT_PATTERNS = [
    b'<<<<<<< ',
    b'======= ',
    b'=======\n',
    b'>>>>>>> ',
]
WARNING_MSG = 'Merge conflict string "{0}" found in {1}:{2}'


def is_in_merge():
    return (
        os.path.exists(os.path.join('.git', 'MERGE_MSG')) and
        (
            os.path.exists(os.path.join('.git', 'MERGE_HEAD')) or
            os.path.exists(os.path.join('.git', 'rebase-apply')) or
            os.path.exists(os.path.join('.git', 'rebase-merge'))
        )
    )


def detect_merge_conflict(argv=None):

    if not is_in_merge():
        return 0

    files = added_files()
    retcode = 0
    for filename in files:
        with open(filename, 'rb') as inputfile:
            for i, line in enumerate(inputfile):
                for pattern in CONFLICT_PATTERNS:
                    if line.startswith(pattern):
                        if retcode == 0:
                            print("***** merge conflict check failed *****")
                        print(WARNING_MSG.format(
                            pattern.decode(), filename, i + 1,
                        ))
                        retcode = 1

    return retcode


if __name__ == '__main__':
    exit(detect_merge_conflict())
