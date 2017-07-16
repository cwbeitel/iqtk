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

import logging
import os
import tempfile
import unittest

from inquiry.framework import gcp

class GCSUtilsTest(unittest.TestCase):

    def test_list_contents(self):

        cases = [
            [
                'gs://inquiry-test/gcs_ops_test/',
                [
                    'gs://inquiry-test/gcs_ops_test/',
                    'gs://inquiry-test/gcs_ops_test/file.txt'
                ]
            ]
        ]

        for c in cases:
            self.assertEqual(gcp.gsutil_list(c[0]),
                             c[1])

    def test_fail_if_spaces(self):

        with self.assertRaises(Exception):
            gcp._fail_if_spaces('/this/is/not/a/great /way/to/ go')

    def test_is_url(self):

        cases = [
            ['gs://some/bucket', 'GCS'],
            ['234://some/bucket', 'Unknown'],
            ['http://some.website.com/files', 'HTTP'],
            ['https://some.website.com/files', 'HTTP'],
            ['some.website.com/files', 'Unknown'],
            ['/tmp/1243edf3/data', 'Local']
        ]
        for c in cases:
            self.assertEqual(gcp._path_type(c[0]), c[1])

    def test_stage_data_wrapper(self):

        error_cases = [
            ['gs://some/bucket', 'https://some.website.com/files'],
            ['/tmp/1243edf3/data', 'https://some.website.com/files'],
            ['http://some.website.com/files', 'some.website.com/files'],
            ['gs://some/bucket', 'gs://some/other/bucket']
        ]
        for ec in error_cases:
            with self.assertRaises(ValueError):
                gcp.stage_data(ec[0], ec[1])

    def test_local_dir_stage_data(self):

        prefix_cases = [
            ['/tmp/iq', '/tmp/123', True],
            ['/tmp/iq', '/iq', True],
            ['/dev/something/large', '/tmp/iq', True],
            ['/tmp/iq1234', '/tmp/iq/1234', False],
            ['/tmp/iq', '/tmp/iq', False]
        ]

        # Local setup
        if not os.path.exists('/tmp/iq'):
            os.system('mkdir /tmp/iq')

        for c in prefix_cases:
            if c[2]:
                with self.assertRaises(ValueError):
                    gcp._local_dir_stage_data(c[0], c[1])
            else:
                source = tempfile.mkdtemp(prefix=c[0])
                target = tempfile.mkdtemp(prefix=c[1])
                with open(source + '/file.txt', 'w') as f:
                    f.write('helloworld')
                gcp._local_dir_stage_data(source + '/file.txt', target)
                self.assertTrue(os.path.exists(target + '/file.txt'))


    def test_stage_data_round_trip(self):

        test_bucket_stem = 'gs://inquiry-test/tests/stage_data_round_trip'
        test_bucket_cases = test_bucket_stem + '/cases'

        fname_cases = [
            'file.txt'
        ]

        for c in fname_cases:

            remote_fname = test_bucket_cases + '/' + c
            dummy = tempfile.mkdtemp(prefix='/tmp/iq')
            remote_tmp = '%s%s' % (test_bucket_stem, dummy)
            local_tmpdir = tempfile.mkdtemp(prefix='/tmp/iq')

            gcp.stage_data(remote_fname, local_tmpdir)
            gcp.stage_data(local_tmpdir + '/' + c, remote_tmp)
            self.assertEqual(gcp.gsutil_list(remote_tmp),
                             [remote_tmp + '/' + c])

    def test_gcs_get_checksum(self):

        test_stem = 'gs://inquiry-test/tests/verify_remote_checksums'
        CASES = [{
            'location': test_stem + '/case1/f.txt',
            'checksum': 'b1kCrCNwJL3QwXbLkwY9xA==',
            'result': True
            },
            {
            'location': test_stem + '/case1/f.txt',
            'checksum': 'b1kCrCNwJL3QwXbLkwY9xB==',
            'result': False
            }]

        for c in CASES:
            cks = gcp.gcs_get_checksum(c['location'])
            if cks is not c['checksum']:
                logging.debug('%s, %s' % (c, cks))
            res = (c['checksum'] == cks)
            self.assertEqual(res, c['result'])

    def test_file_list_match(self):

        test_set = ['file1.txt', 'file2.txt', 'notfile.txt',
                    'a.bam', 'a.vcf', 'ba.vcf']

        CASES = [
            {'pattern': '^file[0-9]+\.txt',
             'expected': ['file1.txt', 'file2.txt']},
            {'pattern': '[a-z]+\.vcf',
             'expected': ['a.vcf', 'ba.vcf']},
            {'pattern': '^a\.[a-z]+$',
             'expected': ['a.bam', 'a.vcf']},
            {'pattern': '[a-z]+nope[a-z]+',
             'expected': []},
            {'pattern': '[a-z]+',
             'expected': test_set},
        ]

        for c in CASES:
            self.assertEqual(gcp._regex_match_list(test_set, c['pattern']),
                             c['expected'])

    def test_gcs_verify_checksums(self):

        test_stem = 'gs://inquiry-test/tests/verify_remote_checksums'
        CASES = [
            {
                'expected_return': True,
                'location': test_stem + '/case1',
                'expected': [{
                    'pattern': '^f\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                }]
            },
            {
                'expected_return': True,
                'location': test_stem + '/case1',
                'expected': [{
                    'pattern': '^[a-z]+\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                }]
            },
            {
                'expected_return': False,
                'location': test_stem + '/case1',
                'expected': [{
                    'pattern': '^a|b|c\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                }]
            },
            {
                'expected_return': False,
                'location': test_stem + '/case1',
                'expected': [{
                    'pattern': '^f\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xB=='
                },
                {
                    'pattern': '^f\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                }]
            },
            {
                'expected_return': False,
                'location': test_stem + '/case1',
                'expected': [{
                    'pattern': '^non_existent_file.txt',
                    'checksum': '12345wronglength=='
                }]
            },
            {
                'expected_return': False,
                'location': test_stem + '/case3',
                'expected': [{
                    'pattern': 'dir_doesnt_even_exist!!!!g65w44#422$$.txt',
                    'checksum': '12345wronglength=='
                }]
            },
            {
                'expected_return': False,
                'location': test_stem + '/a/b/c/case3',
                'expected': [{
                    'pattern': 'wow this one really doesnt exist spaces though...',
                    'checksum': 'kittens=='
                }]
            },
            {
                'expected_return': True,
                'location': test_stem + '/case2',
                'files': [

                ],
                'expected': [{
                    'pattern': '^f2\.txt',
                    'checksum': 'B5c5YJwY2d32LEuiJXXjDw=='
                },
                {
                    'pattern': '^f\.txt',
                    'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                }]
            },
        ]

        for c in CASES:
            v = gcp.gcs_verify_checksums(c['location'], c['expected'])
            if v is not c['expected_return']:
                logging.debug('failed gcs_veify_cks case: %s, %s' % (c, v))
            self.assertEqual(c['expected_return'], v)


    def test_collect_workflow_outputs(self):

        CASES = [
            {
                'location': ('gs://inquiry-test/tests/collect_workflow_outputs/'
                             'case1/'),
                'file_list': [
                    ('gs://inquiry-test/output/test-e2e-0-20170425194932/'
                     'tophat-20170425194933/accepted_hits.bam')
                ]
            }
        ]

        for c in CASES:
            self.assertEqual(sorted(gcp.collect_workflow_outputs(c['location'])),
                             sorted(c['file_list']))


    def test_verify_workflow_outputs_basic_positive(self):

        c = {
                'output': 'gs://jbei-cloud-iqtk/output/local-workflow-test-simple-20170709154647/',
                'expected': [
                    {
                        'pattern': '^f\.txt',
                        'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='
                    }
                ],
                'assessment': True
            }

        self.assertEqual(c['assessment'],
                         gcp.verify_workflow_outputs(c['output'],
                                                     c['expected']))


    def test_verify_workflow_outputs_basic_negative(self):
        c = {
                'output': 'gs://jbei-cloud-iqtk/output/local-workflow-test-simple-20170709154647/',
                'expected': [
                    {
                        'pattern': '^f\.txt',
                        'checksum': 'c1kCrCNwJL3QwXbLkwY9xA=='
                    }
                ],
                'assessment': False
            }

        self.assertEqual(c['assessment'],
                         gcp.verify_workflow_outputs(c['output'],
                                                     c['expected']))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
