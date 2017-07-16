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
"""Argument handling tests."""

import unittest
import json
import tempfile

# 
# class LoadConfigTest(unittest.TestCase):
#
#     def test_config_loader(self):
#         """
#         Tests some thing in detail with precision
#         """
#         cfg = {'key1': 'value1',
#                    'key2': ['value21', 'value22'],
#                    'key3': {'key31': 'value311'}}
#
#         TEST_CASES = [
#             {
#                 'params': cfg,
#                 'expected': {
#                     'value': cfg,
#                     'errors': []
#                     }
#             }
#         ]
#
#         for case in TEST_CASES:
#
#             f = tempfile.NamedTemporaryFile(delete=False)
#             json.dump(case['params'], f)
#             f.close()
#             cfg = load_config(f.name)
#             self.assertEqual(cfg, case['params'])
