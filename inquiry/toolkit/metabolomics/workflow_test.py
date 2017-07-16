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
"""Metabolomics workflow tests"""

import unittest

import inquiry.framework as iqf

from inquiry.toolkit.metabolomics.workflow import ConvertWorkflow
from inquiry.toolkit.metabolomics.workflow import XCMSPreprocess


E2E_CASES = [
    # Should be able to work with either .d or .d.tgz and should yield
    # a file named converted.mzML with a consistent checksum.
    # {
    #     'op': ConvertWorkflow,
    #     'config': {
    #       "archives": [
    #           "gs://inquiry-test/tests/toolkit-ms/file.tgz"
    #       ]
    #     },
    #     'expected': [
    #         {
    #             'pattern': '\.mzML$',
    #             'checksum': 'qC9nKuC4qiuvmN7svF6Adg=='
    #         }
    #     ]
    # },
    # {
    #     'op': ConvertWorkflow,
    #     'config': {
    #       "agilent_d_files": [
    #           "gs://inquiry-test/tests/toolkit-ms/file.d"
    #       ]
    #     },
    #     'expected': [
    #         {
    #             'pattern': '\.mzML$',
    #             'checksum': 'qC9nKuC4qiuvmN7svF6Adg=='
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
