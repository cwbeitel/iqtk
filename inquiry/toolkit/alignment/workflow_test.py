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
"""Alignment workflow tests"""

import unittest

import inquiry.framework as iqf

from inquiry.toolkit.alignment.workflow import AlignmentWorkflow


E2E_CASES = [
    # {
    #     'op': AlignmentWorkflow,
    #     'config': {
    #       "ref_fasta": (
    #             "gs://inquiry-test/tests/toolkit-genotyping/data/genome_small.fa"
    #           ),
    #       "reads": [
    #            ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794486_C2_R1_1_small.fq",
    #             "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794486_C2_R1_2_small.fq"]
    #        ]
    #     },
    #     'expected': [
    #         {
    #             'pattern': '^f\.txt',
    #             'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
    #         }
    #     ]
    # }
]

class WorkflowTest(unittest.TestCase):
    def test_e2e(self):
        for case in E2E_CASES:
            self.assertTrue(iqf.local.e2e_test_runner(case))


if __name__ == "__main__":
    unittest.main()
