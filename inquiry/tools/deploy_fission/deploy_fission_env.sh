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

export FISSION_URL=http://$(kubectl --namespace fission get svc controller -o=jsonpath='{..ip}')
export FISSION_ROUTER=$(kubectl --namespace fission get svc router -o=jsonpath='{..ip}')

ENV_NAME=iqtk-fission-env
ENV_VERSION=0.0.1
ENV_TAG=quay.io/iqtk/${ENV_NAME}:${ENV_VERSION}
FUNC_NAME=funcy
FUNC_ROUTE=${FUNC_NAME}

# Create the environment and delete the previous if necessary
if [[ "$(fission env list | grep ${ENV_NAME})" ]]; then
  fission env delete --name ${ENV_NAME}
fi
fission env create --name ${ENV_NAME} --image ${ENV_TAG}
