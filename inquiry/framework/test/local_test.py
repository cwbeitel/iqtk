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
"""Local container run tests."""

import apache_beam as beam
import unittest
import datetime
import tempfile
import logging
import json
import sys

from inquiry.framework import local
from inquiry.framework import gcp
from inquiry.framework import util
from inquiry.framework import task
from inquiry.framework import workflow

def write_conf(conf):

    assert isinstance(conf, dict)

    tf = tempfile.NamedTemporaryFile(delete=False)
    tf.writelines([json.dumps(conf)])
    tf.close()
    DUMMY_CONF = tf.name
    return DUMMY_CONF


# def local_dev_op(pc, args, label="local_test_op", tag=None):
#     label = update_label_if_tag(label, tag)
#     res = (pc
#            | dev_ladd(label, 'crun') >> beam.FlatMap(_local_dev_op,
#                                                      args=args)
#            | dev_ladd(label, 'wait') >> beam.FlatMap(poll_until_complete)
#            | dev_ladd(label, 'verify') >> beam.FlatMap(verify))
#
#     if workflow.debug:
#         write_dev(util.dev_fc_to_dict(res), workflow.output, dev_ladd(label, tag))
#
#     return res


# def _local_dev_op(read_pair, args, disk=20, cpu_cores=8, ram=8, subset=None,
#                   out_path='/mnt/data/output'):
#
#     inputs = []
#
#     cmd = build_cmd(['echo', '"hello world"', '>', '/mnt/data/output/f.txt'])
#
#     out = crun(cmd, ram=ram, subset=subset, args=args, disk=disk,
#                inputs=inputs, optag='tophat', cpu_cores=cpu_cores,
#                image='gcr.io/jbei-cloud/alignment:0.0.1')
#
#     subset_output_dir = out['subset_output_dir']
#
#     output_files = [
#         File(file_type='txt',
#              remote_path=localize('f.txt', local_stem=subset_output_dir))
#     ]
#
#     out['output_files'] = output_files
#
#     yield out


# def dev_workflow_single_op(args, p):
#
#     reads = util.fc_create(p, ['somefile'])
#     align_out = local_dev_op(reads, args)
#     write_workflow_outputs(util.dev_fc_to_dict(align_out), workflow.output)
#     return align_out


# def write_workflow_outputs(outputs, out_dir):
#     write_dev(outputs, out_dir, '_workflow-outputs')


# def dev_workflow_chained_ops(args, p):
#
#     reads = util.fc_create(p, ['somefile'])
#     align_out = local_dev_op(reads, args)
#     align_out2 = local_dev_op(align_out, args)
#     write_workflow_outputs(util.dev_fc_to_dict(align_out2), workflow.output)
#     return align_out2


class LocalDevOp(task.ContainerTask):
    def __init__(self, args):
        """Initialize a containerized task."""
        container = task.ContainerTaskResources(
            disk=60, cpu_cores=4, ram=8,
            image='gcr.io/jbei-cloud/alignment:0.0.1')
        super(LocalDevOp, self).__init__(task_label='local-dev-op-test',
                                         args=args,
                                         container=container)

    def process(self, file_path):
        cmd = util.Command(['echo "hello world" > /mnt/data/output/f.txt'])
        yield self.submit(cmd.txt, inputs=[],
                          expected_outputs=[{'name': 'f.txt', 'type': 'txt'}])


class SimpleWorkflow(workflow.Workflow):
    """Quantify transcript levels using the Tophat/Cufflinks/Cuffdiff pipeline."""

    def __init__(self):
        """Initialize a workflow."""
        self.tag = 'local-workflow-test-simple'
        self.arg_template = {

        }
        super(SimpleWorkflow, self).__init__()

    def define(self):
        reads = util.fc_create(self.p, ['somefile'])
        result = (reads | task.ContainerTaskRunner(LocalDevOp(args=self.args)))
        #write_workflow_outputs(util.dev_fc_to_dict(result), workflow.output)
        return result


class LocalDockerTaskTest(unittest.TestCase):

    def setUp(self):

        self.TEST_BUCKET = 'gs://inquiry-test'

        # tf = tempfile.NamedTemporaryFile(delete=False)
        # tf.writelines([json.dumps({'local': True})])
        # tf.close()
        # self.DUMMY_CONF = write_conf({'local': True})
        #
        # self.ram = 4
        # self.disk = 20
        # self.cores = 4
        # self.dry_run = False
        # self.image = 'gcr.io/jbei-cloud/alignment:0.0.1'
        # self.command = 'pwd'
        # self.inputs = []
        #
        # TAG = 'local-docker-test'
        # self.args, self.p = workflow.parse_arguments(job_tag=TAG,
        #                                      bucket=self.TEST_BUCKET,
        #                                      arg_template={},
        #                                      config=self.DUMMY_CONF)
        #
        # # self.workflow.local = True
        # # self.workflow.debug = True
        # # self.workflow.dry_run = False
        #
        # self.job_spec = {
        #             'input_files': self.inputs, 'log_output_path': self.workflow.output_dir,
        #             'disk_size': self.disk, 'min_ram': self.ram, 'command': self.command,
        #             'project_id': self.workflow.project, 'runtime_image': self.image, 'job_args': {},
        #             'job_name': self.workflow.job_name, 'region': 'us-central1-f',
        #             'dry_run': self.dry_run, 'output_dir': self.workflow.output_dir, 'cpu_cores': self.cores,
        #             'timeout': datetime.timedelta(hours=3)
        #         }


    # def test_local_run(self):
    #
    #     job_spec = self.job_spec
    #     job_spec['command'] = 'pwd && pwd'
    #     res = local_run(**job_spec)
    #     self.assertEqual(res['logs'], '/data\n/data\n')
    #
    #
    # def test_local_run_fails(self):
    #
    #     job_spec = self.job_spec
    #     job_spec['command'] = 'asdfghjk'
    #     with self.assertRaises(Exception):
    #         local_run(**job_spec)


    def test_e2e_verify_workflow_simple(self):

        c = {'op': SimpleWorkflow,
             'config': {
                 "ref_fasta": "gs://some/file"
             },
             'expected': [
                 {'pattern': '^f\.txt',
                  'checksum': 'b1kCrCNwJL3QwXbLkwY9xA=='}
                ]
            }

        self.assertTrue(local.e2e_test_runner(c))

    def test_e2e_verify_workflow_simple_successful_fail(self):

        c = {'op': SimpleWorkflow,
             'config': {},
             'expected': [
                 {'pattern': '^f\.txt',
                  'checksum': 'c1kCrCNwJL3QwXbLkwY9xA=='}
                ]
            }

        self.assertFalse(local.e2e_test_runner(c))



    # def test_e2e_verify_workflow(self):
    #
    #     for i, case in enumerate(E2E_CASES):
    #
    #         #from apache_beam.transforms.util import assert_that
    #         import time
    #
    #         tag = 'test-e2e-%d' % i
    #         conf = write_conf(case['config'])
    #         args, p = prepare_pipeline(job_tag=tag, bucket=self.TEST_BUCKET,
    #                                    arg_template={},
    #                                    config=conf)
    #         workflow.local = True
    #         workflow.debug = True
    #         workflow.dry_run = False
    #         result = case['op'](args, p)
    #         #assert_that(result, beam.equal_to([True]))
    #         p.run()
    #
    #         verified = verify_workflow_outputs(workflow.output, case['expected'])
    #
    #         if not verified:
    #             logging.info('==FAILED e2e checksum verify for case: %s' % case)
    #         self.assertTrue(verified)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
