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
"""Workflow tests"""

import unittest

import inquiry.framework as iqf

from inquiry.toolkit.genotyper_gatk.workflow import GenotypeGATKWorkflow


E2E_CASES = [
    # {
    #     'op': GenotypeGATKWorkflow,
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
    #
    #         # The bcf and vcf results are checksum-nondeterministic so this
    #         # means of verification does not work. But we can convert this to
    #         # testing either for a checksum or more generally for the existence
    #         # of a file and perhaps that it has nonzero size or size over or in
    #         # a specified range.
    #         # {
    #         #     'pattern': '^var\.flt\.vcf',
    #         #     'checksum': 'CH7Am1yn/jpxUs1aue1Wog=='
    #         # },
    #         # {
    #         #     'pattern': '^var\.raw\.bcf',
    #         #     'checksum': 'kJUuhOwzR8GrKDsiRg79Rw=='
    #         # },
    #         # {
    #         #     'pattern': '^metrics\.txt',
    #         #     'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
    #         # },
    #
    #         {
    #             'pattern': '^sorted\.deduped\.bam$',
    #             'checksum': 'LEOaPU9kdDd8AI/ViyTcgQ=='
    #         },
    #         {
    #             'pattern': '^sorted\.deduped\.bai',
    #             'checksum': 'BOIBdZyDgIKoDmgE7CBmfg=='
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
