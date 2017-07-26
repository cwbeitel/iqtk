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

# Deploy core
kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-rbac.yaml --validate=false
kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-cloud.yaml --validate=false

# Deploy UI
kubectl create -f https://raw.githubusercontent.com/fission/fission-ui/master/docker/fission-ui.yaml --validate=false

# Deploy NATS
kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-nats.yaml --validate=false
