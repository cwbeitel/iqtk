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
"""Command-line interface"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class Client(object):
    """The IQTK client object."""

    def _validate_run_request(self, config):
        pass

    def run(self, config):
        msg = self._validate_run_request(config)
        if msg is not None:
            return msg


class WorkflowServiceWrapper(object):


    def __init__(self, topic_name='dev-topic', sub_name='dev-sub'):

        # Instantiate the PubSub client, topic, and subscriptions.
        self.ps_client = pubsub.Client()
        self.topic = self.ps_client.topic(topic_name)
        if not self.topic.exists():
            self.topic.create()
        self.subscription = self.topic.subscription(sub_name)
        if not self.subscription.exists():
            self.subscription.create()

        # Instantiate the IQTK client
        self.iqtk_client = IQTKClient()


    def _workflow_config_for_sync_message(self):
        pass


    def _pubsub_receive(self):
        """Receives a message from a pull subscription."""
        results = self.subscription.pull(return_immediately=False)
        print('Received {} messages.'.format(len(results)))
        for ack_id, message in results:
            print('* {}: {}, {}'.format(
               message.message_id, message.data, message.attributes))
        if results:
            self.subscription.acknowledge([ack_id for ack_id, message in results])


    def listen(self):
        while True:
            msg = self.pubsub_receive()
            cfg = _workflow_config_for_sync_message(msg)
