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


class MiSeqSequencingRun(object):
    """Representation of config, logs, and results for a sequencing run."""

    def __init__(self, config=None):
        self.config = config

    def _mock_setup(self, num_samples=5):
        self.num_samples = num_samples
        # Ensure instrument data root path exists
        os.system('mkdir -p %s' % self.instrument_data_root)
        # Create a working directory for the run data
        self.workdir = tempfile.mkdtemp(dir=self.instrument_data_root)
        # Make a super realistic sample sheet i.e. SampleSheet
        os.system('touch %s' % os.path.join(self.workdir, 'SampleSheet.csv'))

    def _mock_cycles(self, num_cycles=20, num_spots=20):
       # Make a bunch of pretend images?
        logging.info('mocking miseq sequencing cycles')
        for i in range(1, num_cycles):
            stem = os.path.join(self.workdir, 'Images/L001/C%s' % i)
            os.system('mkdir -p %s' % stem)
            for j in range(1, num_spots):
                os.system('touch %s' % os.path.join(stem, '%s.jpg' % str(uuid.uuid4())))

    def _mock_analysis(self):
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

    def mock_run(self):
        self._mock_setup()
        self._mock_cycles()
        self._mock_analysis()

    def reconstruct(self):
        """Reconstruct from an output directory."""
        pass


class MiSeq(base.IOTDevice):

    def __init__(self, instrument_data_root='/tmp/iq/MISEQ'):
        self.instrument_data_root = instrument_data_root

    def mock_run(self, config):
        run = MiSeqSequencingRun(config)
        run.mock_run()
        return run
