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
"""Prototype models of MiSeq device, events, and message-to-event handler."""

from inquiry.iot import base
import os
import tempfile
import logging
import uuid

from inquiry.iot.models import miseq_pb2
from inquiry.iot import util


class MiSeqSequencingRun(object):

    def __init__(self, run_workdir):
        """Initialize.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

        """
        self.run_workdir = run_workdir

    def reconstruct(self):
        pass

    def _mock(self):

        self.num_samples = num_samples
        # Ensure instrument data root path exists
        os.system('mkdir -p %s' % self.instrument_data_root)
        # Create a working directory for the run data
        self.workdir = tempfile.mkdtemp(dir=self.instrument_data_root)
        # Make a super realistic sample sheet i.e. SampleSheet
        os.system('touch %s' % os.path.join(self.workdir, 'SampleSheet.csv'))

       # Make a bunch of pretend images?
        logging.info('mocking miseq sequencing cycles')
        for i in range(1, num_cycles):
            stem = os.path.join(self.workdir, 'Images/L001/C%s' % i)
            os.system('mkdir -p %s' % stem)
            for j in range(1, num_spots):
                os.system('touch %s' % os.path.join(stem, '%s.jpg' % str(uuid.uuid4())))

        # Mock an analysis stdout and stderr
        for i in range(0, self.num_samples):
            stem = os.path.join(self.workdir, 'Data/Intensities/BaseCalls/')
            os.system('mkdir -p %s' % stem)
            mock_fq1 = os.path.join(stem, '%s_R1_001.fastq.gz' % str(uuid.uuid4()))
            mock_fq2 = os.path.join(stem, '%s_R2_001.fastq.gz' % str(uuid.uuid4()))
            os.system('touch %s' % mock_fq1)
            os.system('touch %s' % mock_fq2)

        os.system('touch %s' % os.path.join(self.workdir, 'AnalysisLog.txt'))
        os.system('touch %s' % os.path.join(self.workdir, 'AnalysisError.txt'))


class MiSeq(object):
    """A MiSeq instrument/device model.

    While currently this only stores the instrument data root, conceptually a
    device is distinct from an instance of the application of that device (i.e
    a device run). The device itself has a location, unique name/id, history,
    running state, associated data streams, etc. Provided the ID of a device
    we should be able to call up a current device model that has associated
    with it a history of device runs/actions and configuration.
    """

    def __init__(self, instrument_data_root='/tmp/iq/MISEQ'):
        self.instrument_data_root = instrument_data_root


def _parse_config_section_name(line):
    ALLOWED_SECTION_NAMES = ['Header', 'Reads', 'Settings', 'Data']
    section = line.strip().split('[')[1].split(']')[0]
    if section not in ALLOWED_SECTION_NAMES:
        raise ValueError('section %s not in set of allowed names, %s'
                         % (section, ALLOWED_SECTION_NAMES))
    if not isinstance(section, str):
        logging.error('section name must be a string')
    elif len(section) == 0:
        logging.error('section name string must be non-empty')
    return section


def update_miseq_sample_given_line(sample, line):
    """Parses a sample sheet sample description line into a MiSeqSample."""
    arr = line.split(',')
    sample.sample_id = arr[0]
    sample.sample_plate = arr[1]
    sample.sample_well = arr[2]
    sample.i7_index_id = arr[3]
    sample.index = arr[4]
    sample.sample_project = arr[5]
    sample.description = arr[6]


def miseq_run_config_from_local_path(path):
    # Probably should be able to obtain type of pb2 object field and cast to
    # whatever that is...
    parser_key_mapping = {
        'IEMFileVersion': ['iem_file_version', int],
        'InvestigatorName': ['investigator_name', str],
        'ExperimentName': ['experiment_name', str],
        'Date': ['date', str],
        'Workflow': ['workflow', str],
        'Application': ['application', str],
        'Assay': ['assay', str],
        'Description': ['description', str],
        'Chemistry': ['chemistry', str],
        'Adapter': ['read_1_adapter', str],
        'AdapterRead2': ['read_2_adapter', str]
    }
    if not isinstance(path, str):
        raise ValueError('path must be an instance of str, saw %s' % path)

    run_config = miseq_pb2.MiSeqRunConfig()
    with open(path, 'r') as f:
        lines = f.read().split('\r')
        section = None
        read_length_lines_seen = 0
        for line in lines:
            if not isinstance(line, str) or len(line) == 0:
                continue
            if line[0] == '[':
                section = _parse_config_section_name(line)
            elif section in ['Header', 'Settings']:
                arr = line.split(',')
                # Strip spaces, e.g. "Investigator Name" => "InvestigatorName"
                key = arr[0].replace(" ", "")
                if key not in parser_key_mapping:
                    # TODO: Do we want to raise a value error instead?
                    logging.info('Encountered unrecognized attribute key, '
                                 '%s, skipping.' % arr[0])
                    continue
                attr = parser_key_mapping[key][0]
                ty = parser_key_mapping[key][1]
                setattr(run_config, attr, ty(arr[1]))
            elif section == 'Reads':
                if read_length_lines_seen == 0:
                    run_config.read_1_length = int(line.split(',')[0])
                elif read_length_lines_seen == 1:
                    run_config.read_2_length = int(line.split(',')[0])
                else:
                    # Handle observing more than 2 non-null lines?
                    continue
                read_length_lines_seen += 1
            elif section == 'Data':
                arr = line.split(',')
                if arr[0] is not None and arr[0] is not 'Sample_ID':
                    sample = run_config.samples.add()
                    update_miseq_sample_given_line(sample, line)

    return run_config


def miseq_run_config_from_gcs_path(gcs_path):
    tempdir = tempfile.mkdtemp()
    util.gsutil_cp_single(gcs_path, tempdir)
    local_path = os.path.join(tempdir, gcs_path.split('/')[-1])
    logging.info(local_path)
    run_config = miseq_run_config_from_local_path(local_path)
    return run_config


def sync_message_indicates_ready_for_analysis(sync_message):
    """Determines whether a GCS sync message indicates sequencing is complete.

    TODO: There are a few issues here primarily that in syncing old run dirs
    we may sync the MiSeq ready for analysis signal file before the FASTQ files.

    Args:
        sync_message (str): A GCS storage sync message to interpret as to
            whether the need for analysis is indicated.

    Returns:
        bool: Whether the provided message designates readiness for analysis.

    """
    pass
