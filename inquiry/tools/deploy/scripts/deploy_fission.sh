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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/deploy_common.sh"

ensure_kube_cluster_exists

function main() {

  # Unset in case of prior deployments
  export FISSION_URL=''
  export FISSION_ROUTER=''

  # Deploy core
  # TODO: Check for existing deployment, delete if exists?
  kubectl create -f ${SCRIPT_DIR}/../configs/fission-rbac.yaml --validate=false
  kubectl create -f ${SCRIPT_DIR}/../configs/fission-cloud.yaml --validate=false

  while true; do
    echo 'Waiting for fission to start...'
    export FISSION_URL=http://$(kubectl --namespace fission get svc controller -o=jsonpath='{..ip}')
    export FISSION_ROUTER=$(kubectl --namespace fission get svc router -o=jsonpath='{..ip}')
    if [[ ${FISSION_URL} && ${FISSION_ROUTER} ]]; then break; fi
    sleep 5
  done

  # Deploy NATS
  kubectl create -f ${SCRIPT_DIR}/../configs/fission-nats.yaml --validate=false

  # Deploy logger
  kubectl create -f ${SCRIPT_DIR}/../configs/fission-logger.yaml --validate=false

  # Deploy UI
  kubectl create -f ${SCRIPT_DIR}/../configs/fission-ui.yaml --validate=false

  echo "finished deploying fission. to use the fission cli, set the following:"
  echo "export FISSION_URL=http://$(kubectl --namespace fission get svc controller -o=jsonpath='{..ip}')"
  echo "export FISSION_ROUTER=$(kubectl --namespace fission get svc router -o=jsonpath='{..ip}')"

}


main "$@"
