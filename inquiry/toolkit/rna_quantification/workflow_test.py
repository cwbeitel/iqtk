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

# class OperationsTest(unittest.TestCase):
#
#     def setUp(self):
#
#         self.ref_fasta = 'gs://inquiry-test/tests/toolkit-genotyping/data/genome_small.fa'
#         self.genes_gtf = 'gs://inquiry-test/tests/toolkit-expression/data/genes_small.gtf'
#         self.cond_a_pairs = [[
#             "gs://inquiry-test/tests/toolkit-expression/data/reads_c1_1_vsmall.fq",
#             "gs://inquiry-test/tests/toolkit-expression/data/reads_c1_2_vsmall.fq"
#             ]]
#         self.cond_b_pairs = [[
#             "gs://inquiry-test/tests/toolkit-expression/data/reads_c2_1_vsmall.fq",
#             "gs://inquiry-test/tests/toolkit-expression/data/reads_c2_2_vsmall.fq"
#             ]]
#
#     def test_tophat(self):
#
#         class TopHatOpTestFlow(Workflow):
#
#             def __init__(self, operation):
#                 self.operation = operation
#                 self.tag = 'test-operation-%s' % operation.__name__
#                 self.arg_template = {
#                     'single_input': {'help': 'a single input file'}
#                 }
#                 super(SingleInputWrapperWorkflow, self).__init__()
#
#             def define(self):
#                 return (util.fc_create(self.p, self.args.single_input) |
#                         task.ContainerTaskRunner(self.operation(args=self.args)))
#
#         c = {'op': TopHatOpTestFlow,
#              'config': {
#                  'ref_fasta': self.ref_fasta,
#                  'genes_gtf': self.genes_gtf,
#                  'single_input': self.cond_a_pairs[0]
#              },
#              'expected': [
#                  {'pattern': '??',
#                   'checksum': '??'}
#                  ]
#              }
#
#         self.assertTrue(iqf.local.e2e_test_runner(c))
#
#     def test_cufflinks(self):
#
#         c = {'op': iqf.workflow.op_wrapper_factory(ops.Cufflinks),
#              'config': {
#                  'aligned_reads': '??'
#              },
#              'expected': [
#                  {'pattern': 'accepted_hits.bam'},
#                  {'pattern': 'align_summary.txt'},
#                  {'pattern': 'deletions.bed'},
#                  {'pattern': 'insertions.bed'},
#                  {'pattern': 'junctions.bed'},
#                  {'pattern': 'prep_reads.info'}]
#              [
#                  {'pattern': '??',
#                   'checksum': '??'}
#                  ]
#              }
#
#         self.assertTrue(iqf.local.e2e_test_runner(c))
#
#     def test_cuffmerge(self):
#
#         c = {'op': iqf.workflow.op_wrapper_factory(ops.CuffMerge),
#              'config': {
#                  'ref_fasta': 'a',
#                  'genes_gtf': 'b',
#                  'assemblies': 'c'
#              },
#              'expected': [
#                  {'pattern': '??',
#                   'checksum': '??'}
#                  ]
#              }
#
#         self.assertTrue(iqf.local.e2e_test_runner(c))
#
#     def test_cuffdiff(self):
#
#         c = {'op': iqf.workflow.op_wrapper_factory(ops.CuffDiff),
#              'config': {
#              },
#              'expected': [
#                  {'pattern': '??',
#                   'checksum': '??'}
#                  ]
#              }
#
#         self.assertTrue(iqf.local.e2e_test_runner(c))


class WorkflowTest(unittest.TestCase):

    def test_e2e_vsmall(self):
        pass
        # c = {'op': TranscriptomicsWorkflow,
        #      'config': {
        #          "ref_fasta": "gs://inquiry-test/tests/toolkit-genotyping/data/genome_small.fa",
        #          "genes_gtf": "gs://inquiry-test/tests/toolkit-expression/data/genes_small.gtf",
        #          "cond_a_pairs": [
        #              ["gs://inquiry-test/tests/toolkit-expression/data/reads_c1_1_vsmall.fq",
        #               "gs://inquiry-test/tests/toolkit-expression/data/reads_c1_2_vsmall.fq"]
        #              ],
        #          "cond_b_pairs": [
        #              ["gs://inquiry-test/tests/toolkit-expression/data/reads_c2_1_vsmall.fq",
        #               "gs://inquiry-test/tests/toolkit-expression/data/reads_c2_2_vsmall.fq"]
        #              ]
        #          },
        #      'expected': [
        #          {'pattern': '^f\.txt',
        #           'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='}
        #          ]
        #      }
        #
        # self.assertTrue(iqf.local.e2e_test_runner(c))


if __name__ == "__main__":
    unittest.main()
