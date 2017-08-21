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

from inquiry.iot import miseq


class MiSeqSequencingRunTest(unittest.TestCase):
    """Tests of object for representing miseq sequencing run metadata."""

    def test_reconstruct(self):
        """Test of reconstruction from path."""

        cases = [{
            'path': ('gs://iqtk-test-public/iot/miseq/'
                     'test_miseq_sequencing_run/run001'),
            'expected': {
                'num_read_pairs': 12,
                'run_id': 123
            }
        }]

        for c in cases:

            # Reconstruct a representation of that run
            r = miseq.SequencingRun().reconstruct(c['path'])

            for key, value in c['expected']:
                self.assertTrue(hasattr(r, key))
                self.assertEqual(getattr(r, key), value)


class MiSeqTest(unittest.TestCase):

    def init_test(self):
        m = MiSeq()


def _miseq_mock_and_upload(config):
    """Mock a MiSeq run from a config and upload the result.

    Given a config dictionary, run a MiSeq device mock, upload the result,
    and return the path on cloud storage to the uploaded files.

    Args:
        config (dict): The config parameterizing the mock run.

    Returns:
        object: A MiSeqSequencingRun object.
        str: The path on cloud storage where the mocked run was uploaded.
    """
    # Configure the MiSeq device object
    m = MiSeq()

    # Perform a mock run
    sequencing_run = m.mock_run(config)

    # Choose a GCS root path for file uploads.
    remote_dest_base = 'gs://iqtk-test-public/iot/miseq/mock_and_upload_test'

    remote_dest = util.upload(sequencing_run.local_path, remote_dest_base)

    return sequencing_run, remote_dest


class MiSeqRunAndReconstructTest(unittest.TestCase):

    def mock_upload_reconstruct_test(self):
        """Complex test of reconstructing config used for a MiSeq mock run."""
        cases = [
            {
                'contact': 'billy@lbl.gov'
            },
            {
                'contact': 'bobby@lbl.gov'
            }
        ]

        for c in cases:
            run_truth, run_remote_base_path = _miseq_mock_and_upload(c)
            run = miseq.SequencingRun().reconstruct(run_remote_base_path)
            self.assertEqual(run_truth, run)
