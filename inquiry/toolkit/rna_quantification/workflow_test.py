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
"""Expression workflow tests"""

import unittest

import inquiry.framework as iqf

from inquiry.toolkit.rna_quantification import operations as ops
from inquiry.toolkit.rna_quantification.workflow import TranscriptomicsWorkflow


class WorkflowTest(unittest.TestCase):

    def test_e2e_vsmall(self):
        c = {'op': TranscriptomicsWorkflow,
             'config': {
                 "cloud": True,
                 "ref_fasta": "gs://inquiry-test/tests/toolkit-genotyping/data/genome_small.fa",
                 "genes_gtf": "gs://inquiry-test/tests/toolkit-expression/data/genes_small.gtf",
                 "cond_a_pairs": [
                     ["gs://inquiry-test/tests/toolkit-expression/data/reads_c1_1_vsmall.fq",
                      "gs://inquiry-test/tests/toolkit-expression/data/reads_c1_2_vsmall.fq"]
                     ],
                 "cond_b_pairs": [
                     ["gs://inquiry-test/tests/toolkit-expression/data/reads_c2_1_vsmall.fq",
                      "gs://inquiry-test/tests/toolkit-expression/data/reads_c2_2_vsmall.fq"]
                     ]
                 },
             'expected': [
                 {'pattern': '^f\.txt',
                  'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='}
                 ]
             }

        self.assertTrue(iqf.local.e2e_test_runner(c))


if __name__ == "__main__":
    unittest.main()
