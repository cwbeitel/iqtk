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

from inquiry.toolkit.trigger_tester.workflow import SimpleWorkflow


class WorkflowTest(unittest.TestCase):

    def test_e2e_vsmall(self):
        pass
#         c = {'op': SimpleWorkflow,
#              'config': {
#                  "file_path": "gs://inquiry-test/tests/toolkit-genotyping/data/genome_small.fa",
#                  "scalar_param": "7",
#                  },
#              'expected': [
#                 #  {'pattern': '^count\.txt',
#                 #   'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='}
#                  ]
#              }
#
#         self.assertTrue(iqf.local.e2e_test_runner(c))


if __name__ == "__main__":
    unittest.main()
