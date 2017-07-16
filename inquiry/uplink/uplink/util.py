# Copyright 2017 The Regents of the University of California
#
# Licensed under the BSD-3-clause license (the "License"); you may not
# use this file except in compliance with the License.
# You are provided a copy of the license in LICENSE.md at the root of
# this project.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Uplink utilities."""

import os

import subprocess
from subprocess import CalledProcessError

from uplink.log import Logger

LOGGING_LEVEL = 'INFO'

logger = Logger()


def _require_string(variable, issuer):
    if not isinstance(variable, str):
        raise ValueError('%s expects command parameter to be a '
                         'string, saw %s of type %s' % (issuer,
                                                        variable,
                                                        type(variable)))


def _maybe_unicode_to_str(arg):
    if isinstance(arg, unicode):
        return str(arg)
    return arg


def _subprocess(command):
    command = _maybe_unicode_to_str(command)

    logger.debug('subprocess executing command: %s' % command)
    _require_string(command, '_subprocess')

    cmd = subprocess.Popen(command, shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    err = [thing for thing in cmd.stderr]
    out_raw, _ = cmd.communicate()

    if cmd.returncode is 1:
        CalledProcessError(err)

    out = out_raw.strip('\n').split('\n')
    return out


def _require_path_exists(path):
    if not os.path.exists(path):
        msg = 'The requested local path does not exist: %s' % path
        logger.info(msg)
        raise ValueError(msg)


def sync(local_path, remote_bucket_path, exclude=None):
    """Call gsutil rsync, catching and logging errors."""
    _require_path_exists(local_path)

    cmd_str = ' '.join(["gsutil", "-m", "rsync", "-r",
                        local_path, remote_bucket_path])
    logger.debug('sync constructed command: %s' % cmd_str)

    try:
        out = _subprocess(cmd_str)
        logger.debug('sync yielded cmd output: %s' % out)

    except Exception, e:
        logger.error('error with command "%s", raised exception: %s' % (
            cmd_str, e))