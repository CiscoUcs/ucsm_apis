#!/usr/bin/env python
# From https://github.com/pre-commit/pre-commit-hooks
# License: MIT

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess


class CalledProcessError(RuntimeError):
    pass


def exists(cmd):
    out, err, rc = cmd_output('which', '%s' % cmd)
    return rc == 0


def added_files():
    out, err, rc = cmd_output('git', 'diff', '--staged', '--name-only')
    return set(out.splitlines())


def cmd_output(*cmd, **kwargs):
    retcode = kwargs.pop('retcode', 0)
    popen_kwargs = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
    popen_kwargs.update(kwargs)
    proc = subprocess.Popen(cmd, **popen_kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode('UTF-8')
    if stderr is not None:
        stderr = stderr.decode('UTF-8')
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout, stderr, proc.returncode
