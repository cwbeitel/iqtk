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

from inquiry.framework import util


class TestLocalize(unittest.TestCase):
    """Tests some thing in detail with precision."""

    def tests_localizer(self):

        cases = [
            {'example': util.File(file_type='fpkm',
                             local_path=util.localize('genes.fpkm_tracking')),
             'key': '/mnt/data/input/genes.fpkm_tracking'},
            {'example': util.File(file_type='fpkm',
                             local_path=util.localize('genes.fpkm_tracking')),
             'key': '/mnt/data/input/genes.fpkm_tracking'},
            {'example': util.File(file_type='fpkm',
                             local_path=util.localize('genes.fpkm_tracking')),
             'key': '/mnt/data/input/genes.fpkm_tracking'},
            {'example': util.File(file_type='fpkm',
                             local_path=util.localize('genes.fpkm_tracking')),
             'key': '/mnt/data/input/genes.fpkm_tracking'}
            ]

        for c in cases:
            self.assertEqual(c['example'].local_path, c['key'])

# from inquiry.framework import files
#
#
# class TestFile(unittest.TestCase):
#
#     def test_create(self):
#         """Test the creation of a file object."""
#         f = files.File(file_type='bam', condition='a')
#         self.assertEqual(f.condition, 'a')
#
#     def test_update(self):
#         f = files.File(file_type='bam')
#         self.assertEqual(f.condition, None)
#         f.update({'condition': 'a'})
#         self.assertEqual(f.condition, 'a')
#
#     def test_regex_match(self):
#         self.assertTrue(regex_match('bam', '.'))
#         self.assertTrue(regex_match('bam', '.am'))
#         self.assertTrue(regex_match('bam', 'bam'))
#         self.assertFalse(regex_match('bam', 'sam'))
#
#     def test_match(self):
#         """Test whether file meta can be matched given query."""
#         f = files.File(file_type='bam', condition='a')
#         self.assertTrue(f.match({'file_type': 'bam'}))
#         self.assertFalse(f.match({'file_type': 'sam'}))
#         self.assertFalse(f.match({'condition': 'b'}))
#         self.assertTrue(f.match({'condition': 'a'}))
#
#         # Unknown property defaults to false.
#         self.assertFalse(f.match({'unknown': 'kittens'}))
#
#     def test_as_dict(self):
#         f = files.File(file_type='bam', condition='a')
#         self.assertTrue(isinstance(f.as_dict(), dict))
#         self.assertTrue('file_type' in f.as_dict())
#         self.assertEqual(f.as_dict()['file_type'], 'bam')
#
#
# class TestFileCollection(unittest.TestCase):
#
#     def test_create(self):
#         """Test the creation of a file collection from a dict template."""
#         fc = files.FileCollection()
#         # Create a file collection with one member, explicitly
#         fc = files.FileCollection([{'file_type': 'bam'}])
#         self.assertTrue(fc.size() == 1)
#         for f in fc.items():
#             self.assertTrue(isinstance(f, File))
#         self.assertTrue(isinstance(fc.dump(), list))
#         self.assertTrue(len(fc.dump()) == 1)
#         self.assertTrue(isinstance(fc.dump()[0], dict))
#
#     def test_add(self):
#         """Test the addition of a file collection to an existing one."""
#         fc = files.FileCollection()
#         self.assertEqual(fc.size(), 0)
#         fc.add(files.File(template={'file_type': 'bam', 'condition': 'a'}))  # Can add as simple dict
#         self.assertEqual(fc.size(), 1)
#         fc.add(files.File(template={'file_type': 'bam', 'condition': 'b'}))  # Can add as object
#         self.assertEqual(fc.size(), 2)
#         for f in fc.items():
#             self.assertTrue(isinstance(f, File))
#
#     def test_add_paths(self):
#         """Test functionality for adding multiple files all with same meta"""
#         fc = files.FileCollection()
#         cond_a_pairs = ['file/path/one_a.fq', 'file/path/two_a.fq']
#         fc.add_paths(cond_a_pairs, {'condition': 'a'})
#         self.assertEqual(fc.size(), len(cond_a_pairs))
#         for f in fc.items():
#             self.assertTrue(isinstance(f, File))
#
#     def test_as_pcollection(self):
#         pass


if __name__ == "__main__":
    unittest.main()
