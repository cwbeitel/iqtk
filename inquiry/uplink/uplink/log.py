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
"""Hybrid local/cloud logging object."""

import pprint
import sys

import coloredlogs
from google.cloud import logging
import logging as local_logging

LOGGING_LEVEL = 'INFO'


def _require_dict_or_str(message):
    if not isinstance(message, dict) and not isinstance(message, str):
        raise ValueError('logger expects messages to be dictionary or '
                         'string objects, saw: %s, %s' % (type(message),
                                                          message))


def _require_allowed_severity(severity):
    allowed = ["INFO", "DEBUG", "WARN", "ERROR"]
    if severity not in allowed:
        raise ValueError('Severity specified to logger must be one of '
                         '%s, saw %s.' % (allowed, severity))


def _maybe_unicode_to_str(arg):
    if isinstance(arg, unicode):
        return str(arg)
    return arg


class Logger(object):
    """Structured (cloud) logging utility.

    Basic logging object that transparently logs to both the console (for dev)
    and to Google Cloud Logging. Accepts arbitrary message structures, for now.

    Example:

        logging = Logger()
        logging.debug({'text': 'there was an error', 'tag': 1234})

    TODO:
        * Consider standard log message structure w/ proto.

    """

    def __init__(self, severity='INFO', tag=None, log_name='iqtk-uplink'):
        """Instantiate a logging object.

        Args:
            severity (str): Defines the volume of messages that will display.
            tag (str): An optional additional tag to apply to the log_name.
            log_name (str): A Google Cloud Logging log to which to write.
            cloud (bool): Whether to log to the GCL.

        """
        if tag is not None:
            log_name += '-%s' % tag

        _require_allowed_severity(severity)
        self.severity = severity

        self.system_info = self._get_system_info()

        self.cloud_logger = logging.Client().logger(log_name)

        iqtk_logger = local_logging.getLogger(log_name)
        iqtk_logger.setLevel(getattr(local_logging, severity))
        coloredlogs.install(level=severity)
        self.local_logger = iqtk_logger

    def _get_system_info(self):
        return {'python_version': sys.version_info[0]}

    def _add_issuer(self, message):
        if not isinstance(message, dict):
            raise ValueError('Arguments to _add_issuer() should be type dict.')
        message['issuer'] = sys._getframe(4).f_code.co_name
        message['issuer_parent'] = sys._getframe(5).f_code.co_name
        return message

    def debug(self, message):
        """Log a debug-level message."""
        self._log(message, severity='DEBUG')

    def error(self, message):
        """Log an error-level message."""
        self._log(message, severity='ERROR')

    def info(self, message):
        """Log an info-level message."""
        self._log(message, severity='INFO')

    def _log(self, message, severity='INFO'):
        message = self._build_message(message)
        # If we're using cloud logging
        # self.logger.log_struct(self.message, severity='DEBUG')
        getattr(self.local_logger, severity.lower())(message)

    def _build_message(self, message):

        message = _maybe_unicode_to_str(message)

        _require_dict_or_str(message)

        if isinstance(message, str):
            message = {'text': message}

        message = self._add_issuer(message)
        message['system_info'] = self.system_info
        return message

    def _show_locally(self, message):
        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(self.message)
