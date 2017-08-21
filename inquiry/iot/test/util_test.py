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

import unittest
import tempfile
import os

from inquiry.iot import util


def _gcs_file_exists(path):
    """Returns bool whether a file at a specified GCS path exists."""
    # TODO
    return True


class UploadTest(unittest.TestCase):

    def singleton_upload_test(self):
        """Upload a dir with a single file and check it was synced."""

        # Create a temporary directory and write to a file in that dir
        # TODO (use file.txt)
        temp_dir = tempfile.tempdir()
        with open('%s/%s' % (temp_dir, 'file.txt'), 'w') as f:
            f.write('helloworld')

        remote_dir_base = 'gs://iqtk-test-public/iot/util/upload'
        remote_dir = remote_dir_base = temp_dir.split('/')[-1]
        remote_path = util.upload(temp_dir, remote_dir)

        # Verify that the uploaded file exists
        self.assertTrue(_gcs_file_exists(remote_dir + '/file.txt'))


if __name__ == '__main__':
    unittest.main()
