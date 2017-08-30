# Copyright 2017 The Regents of the University of California
#
# Licensed under the BSD-3-clause license (the "License") you may not
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

from inquiry.iot.models import miseq_pb2


class RunConfigTest(unittest.TestCase):

    def test_sample_interface(self):
        """Test of stability of MiSeqSample interface."""
        s = miseq_pb2.MiSeqSample()
        s.sample_id = 'WT_1'
        s.sample_plate = ''
        s.sample_well = ''
        s.i7_index_id = 'A001'
        s.index = 'ATCACG'
        s.sample_project = ''
        s.description = ''
        self.assertTrue(s.IsInitialized())

    def test_init_config(self):
        """Test of stability of MISeqRunConfig interface."""

        c = miseq_pb2.MiSeqRunConfig()
        c.iem_file_version = 1
        c.investigator_name = 'billy the giant'
        c.experiment_name = 'FD_HS_BE_GalS'
        c.date = '12/12/12'
        c.workflow = 'GenerateFASTQ'
        c.application = 'RNA-Seq'
        c.assay = 'TruSeq LT'
        c.description = 'FD(+)-HS(BE+=GalS-*)...'
        c.chemistry = 'Default'
        c.read_1_adapter = 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCA'
        c.read_2_adapter = 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT'
        c.read_1_length = 76
        c.read_2_length = 76

        s = c.samples.add()
        s.sample_id = 'WT_1'
        s.sample_plate = ''
        s.sample_well = ''
        s.i7_index_id = 'A001'
        s.index = 'ATCACG'
        s.sample_project = ''
        s.description = ''
        self.assertTrue(s.IsInitialized())

        # So currently our protos don't have required fields so this doesn't
        # do anything but using protos that allow certain fields to be required
        # wouldn't be a bad idea.
        self.assertTrue(c.IsInitialized())


if __name__ == '__main__':
    unittest.main()
