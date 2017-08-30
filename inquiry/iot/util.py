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

import random
import uuid
import os
import logging

import subprocess
from subprocess import CalledProcessError
import inspect


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

	logging.debug('subprocess executing command: %s' % command)
	_require_string(command, '_subprocess')

	cmd = subprocess.Popen(command, shell=True,
						   stdout=subprocess.PIPE,
						   stderr=subprocess.PIPE)
	err = [thing for thing in cmd.stderr]
	out_raw, _ = cmd.communicate()

	if cmd.returncode is 1:
		raise Exception(err)

	out = out_raw.strip('\n').split('\n')
	return out


def _logged_subprocess(command_string):
	fname = inspect.stack()[1][3]
	logging.debug('%s constructed command: %s' % (fname, command_string))

	try:
		out = _subprocess(command_string)
		logging.debug('%s yielded cmd output: %s' % (fname, out))

	except Exception, e:
		logging.error('error with command "%s", raised exception: %s' % (
			command_string, e))
		raise e


def _require_path_exists(path):
	if not os.path.exists(path):
		msg = 'The requested local path does not exist: %s' % path
		logging.info(msg)
		raise ValueError(msg)


def gsutil_cp_single(file_path, dest_dir):
	"""Copy a single file to or from cloud storage.

	Args:
		file_path (str): The source file path.
		dest_path (str): The destination directory.
	"""
	cmd_str = ' '.join(["gsutil", "cp", file_path, dest_dir])
	_logged_subprocess(cmd_str)


def rsync(source_path, destination_path, exclude=None):
	"""Use rsync to stage a collection of files between two locations.

	Example:
		rsync('/tmp/iq/miseqrun001', 'gs://iqtk-test-public/miseqrun001')

	Notes:
		Currently not clear if there is a better option for uploading a dir to
		GCS. The google-cloud-storage python lib can be used to upload single
		blobs but guessing this will be far slower than `gsutil -m rsync...`?
		Also

	Args:
		source_path (str): The local path of files to rsync.
		destination_path (str): The remote dir on GCS to which to sync files.
	"""
	cmd_str = ' '.join(["gsutil", "-m", "rsync", "-r",
						source_path, destination_path])
	_logged_subprocess(cmd_str)


	# logging.debug('sync constructed command: %s' % cmd_str)
	#
	# try:
	# 	out = _subprocess(cmd_str)
	# 	logging.debug('sync yielded cmd output: %s' % out)
	#
	# except Exception, e:
	# 	logging.error('error with command "%s", raised exception: %s' % (
	# 		cmd_str, e))
	# 	raise e
