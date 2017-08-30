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
import logging
import tempfile

from inquiry.iot import miseq
from inquiry.iot.models import miseq_pb2


def _verify_sample_sheet_test_case(test, run_config):
    test.assertEqual(run_config.iem_file_version, 4)
    test.assertEqual(run_config.investigator_name, 'Solomon Stonebloom')
    test.assertEqual(run_config.experiment_name, 'FD_HS_BE_GalS')
    test.assertEqual(run_config.date, '12/12/14')
    test.assertEqual(run_config.workflow, 'GenerateFASTQ')
    test.assertEqual(run_config.application, 'RNA-Seq')
    test.assertEqual(run_config.assay, 'TruSeq LT')
    test.assertEqual(run_config.description, '')
    test.assertEqual(run_config.chemistry, 'Default')
    test.assertEqual(run_config.read_1_length, 76)
    test.assertEqual(run_config.read_2_length, 76)
    test.assertEqual(run_config.read_1_adapter, 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCA')
    test.assertEqual(run_config.read_2_adapter, 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT')
    test.assertTrue(run_config.IsInitialized())


class ParseRunConfigTest(unittest.TestCase):

    def setUp(self):
        self.sheet_text = """[Header],,,,,,,\rIEMFileVersion,4,,,,,,\rInvestigator Name,Solomon Stonebloom,,,,,,\rExperiment Name,FD_HS_BE_GalS,,,,,,\rDate,12/12/14,,,,,,\rWorkflow,GenerateFASTQ,,,,,,\rApplication,RNA-Seq,,,,,,\rAssay,TruSeq LT,,,,,,\rDescription,,,,,,,\rChemistry,Default,,,,,,\r,,,,,,,\r[Reads],,,,,,,\r76,,,,,,,\r76,,,,,,,\r,,,,,,,\r[Settings],,,,,,,\rAdapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,\rAdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,\r,,,,,,,\r[Data],,,,,,,\rSample_ID,Sample_Name,Sample_Plate,Sample_Well,I7_Index_ID,index,Sample_Project,Description\rWT_1,,,,A001,ATCACG,,\rWT_2,,,,A002,CGATGT,,\r"""

    def test_update_miseq_sample_given_line(self):
        sample = miseq_pb2.MiSeqSample()
        line = 'WT_1,,,,A001,ATCACG,,'
        miseq.update_miseq_sample_given_line(sample, line)
        self.assertEqual(sample.sample_id, 'WT_1')

    def test_miseq_run_config_from_local_path(self):
        """Test of loading sample sheet from CSV path."""
        tempdir = tempfile.mkdtemp()
        ssheet_path = tempdir + '/file.txt'
        with open(ssheet_path, 'w') as f:
            f.write(self.sheet_text)
        logging.info(ssheet_path)
        run_config = miseq.miseq_run_config_from_local_path(ssheet_path)
        _verify_sample_sheet_test_case(self, run_config)

    def test_miseq_run_config_from_gcs_path(self):
        gcs_path = ('gs://iqtk-test-public/iot/miseq/test_miseq_sequencing_run'
                    '/141212_M03257_0002_000000000-AC28N/SampleSheet.csv')
        run_config = miseq.miseq_run_config_from_gcs_path(gcs_path)
        _verify_sample_sheet_test_case(self, run_config)


class MiSeqRunTest(unittest.TestCase):

    def test_miseq_run_from_gcs_path(self):
        """Test of reconstruction of state of miseq run from a GCS path."""
        pass


class SyncResponderTest(unittest.TestCase):

    def test_sync_message_indicates_ready_for_analysis(self):
        cases = [
            {
                'message': {},
                'expected': True
            },
            {
                'message': {},
                'expected': False
            },
        ]
        for c in cases:
            res = miseq.sync_message_indicates_ready_for_analysis(c['message'])
            self.assertEqual(res, c['expected'])


# class MockAndParseRunConfigTest(unittest.TestCase):
#
#     def init_test_miseq(self):
#         m = miseq.MiSeq()
#
#     def init_test_miseq_run(self):
#         m = miseq.MiSeqSequencingRun()
#
#     def test_reconstruct(self):
#         """Test of reconstruction from path."""
#
#         cases = [
#             {
#                 'path': ('gs://iqtk-test-public/iot/miseq/'
#                          'test_miseq_sequencing_run/run001'),
#                 'expected': {
#                     'num_read_pairs': 12,
#                     'run_id': 123
#                 },
#                 'success': True
#             }
#         ]
#
#         for c in cases:
#
#             # Reconstruct a representation of that run
#             run = MiSeqSequencingRun(c['path'])
#             run.reconstruct()
#
#             for key, value in c['expected'].items():
#                 # Verify that the reconstructed run object has the expected
#                 # property values.
#                 logging.info('%s, %s' % (key, value))
#                 self.assertTrue(hasattr(r, key))
#                 #self.assertEqual(getattr(r, key), value)
#
#     def test_mock_upload_reconstruct(self):
#         """Complex test of reconstructing config used for a MiSeq mock run."""
#         cases = [
#             {
#                 'contact': 'billy@lbl.gov'
#             },
#             {
#                 'contact': 'bobby@lbl.gov'
#             }
#         ]
#
#         for c in cases:
#
#             true_run = miseq.MiSeqSequencingRun(c)
#             true_run._mock()
#
#             remote_dest_base = 'gs://iqtk-test-public/iot/miseq/mock_and_upload_test'
#             remote_dest = util.upload(run.workdir, remote_dest_base)
#
#             run = MiSeqSequencingRun(run_remote_base_path)
#             run.reconstruct()
#             self.assertEqual(run_truth, run)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
