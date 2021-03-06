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
"""Testing of API service."""

import unittest
import json

from inquiry.services import api


class APIServiceTest(unittest.TestCase):

    def setUp(self):
        api.app.testing = True
        self.app = api.app.test_client()

    def test_health(self):
        rv = json.loads(self.app.get('/health').data)
        assert 'hp' in rv and rv['hp'] is 100

    def test_list(self):
        # TODO
        pass

    def test_describe(self):
        # TODO
        pass

    def test_delete(self):
        # TODO
        pass

    def test_submit(self):
        # TODO
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
