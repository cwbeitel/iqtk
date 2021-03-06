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

from inquiry.operations.models.db import alignment_pb2


class InterfaceTest(unittest.TestCase):

    def test_interface(self):

        c = alignment_pb2.ReadAlignment()
        # TODO
        #self.assertTrue(r.IsInitialized())


if __name__ == '__main__':
    unittest.main()
