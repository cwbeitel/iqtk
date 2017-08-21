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

deploy_api_kube() {
  export_service_name_id
  local temp_file=$(mktemp)
  export TEMP_FILE="${temp_file}.yaml"
  mv "$temp_file" "$TEMP_FILE"
  < "$CONFIG" sed -E "s/SERVICE-NAME/${ENDPOINTS_SERVICE_NAME}/g" \
    | sed -E "s/SERVICE-CONFIG-ID/${ENDPOINTS_SERVICE_CONFIG_ID}/g" \
    > "${TEMP_FILE}"
  echo "Deploying ${CONFIG} on kubernetes..."
  echo "kubectl create -f ${CONFIG} --validate=false"
  kubectl create -f ${TEMP_FILE} --validate=false
}

cleanup() {
  rm "$TEMP_FILE"
}

# Defaults.
CONFIG="${SCRIPT_DIR}/../configs/api.kube.yaml"

# Cleanup our temporary files even if our deployment fails.
trap cleanup EXIT

deploy_api_kube "$@"
