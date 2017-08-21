#!/usr/bin/env bash
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

TAG=iqtk-api-dev
TOPIC=${TAG}-topic
SUB=${TAG}-sub

echo "Configuring message stream from topic $TOPIC via subscription $SUB..."

if ! [[ $(gcloud alpha pubsub topics list --filter="topicId:$TOPIC") ]]; then
  echo "Topic $TOPIC was not found, creating..."
  gcloud alpha pubsub topics create $TOPIC
fi

if ! [[ $(gcloud alpha pubsub subscriptions list --filter="SUBSCRIPTION=$SUB") ]]; then
  echo "Subscription $SUB was not found, creating..."
  gcloud alpha pubsub subscriptions create $SUB --topic=$TOPIC
fi

echo "Pulling messages from subscription $SUB..."
gcloud alpha pubsub subscriptions pull $SUB --auto-ack
