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
"""Testing of base service object."""

import unittest

from inquiry.services import base


class ServiceTest(unittest.TestCase):

    def test_subclass(self):
        """Trivial test of service subclass pattern."""
        class SomeService(base.Service):
            def run(self):
                logging.info('some service running')


def _sr_maker():
    class SomeServiceOne(base.Service):
        def run(self):
            pass
    class SomeServiceTwo(base.Service):
        def run(self):
            pass
    sr = base.ServiceRegistry({'service_one': SomeServiceOne,
                               'service_two': SomeServiceTwo})
    return sr


class ServiceRegistryTest(unittest.TestCase):

    def test_init_empty(self):
        """Trivial test of instantiation of empty service registry."""
        sr = base.ServiceRegistry({})
        # For now, allow initialization of an empty registry using {} as def.
        sr = base.ServiceRegistry()
        # with self.assertRaises(TypeError):
        #     sr = base.ServiceRegistry()
        with self.assertRaises(TypeError):
            sr = base.ServiceRegistry([])
        with self.assertRaises(TypeError):
            sr = base.ServiceRegistry('kittens')

    def test_init_non_empty(self):
        """Test of init of service registry with Service subclass."""
        sr = _sr_maker()

    def test_recognizes_name(self):
        cases = [
            ['service_one', True, None],
            ['service_two', True, None],
            ['service_three', False, None],
            [12, False, ValueError]
        ]
        sr = _sr_maker()
        for c in cases:
            if c[2] is None:
                self.assertEqual(sr.recognizes_name(c[0]), c[1])
            else:
                with self.assertRaises(c[2]):
                    sr.recognizes_name(c[0])

    def test_must_interface(self):
        """Tests whether a provided service object fits service interface."""
        class NottaService(object):
            pass
        class WorksAsService(object):
            def run(self):
                pass
        class IsAService(base.Service):
            def run(self):
                pass
        sr = base.ServiceRegistry({'kittens': WorksAsService})
        sr = base.ServiceRegistry({'kittens': IsAService})
        with self.assertRaises(TypeError):
            sr = base.ServiceRegistry({'kittens': NottaService})


if __name__ == "__main__":
    unittest.main()
