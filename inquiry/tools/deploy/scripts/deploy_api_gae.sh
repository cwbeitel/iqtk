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

function deploy_api_gae() {

  export TMPDIR=$(mktemp -d -t tmp.XXXXXXXXXX)

  echo $(date) : "=== Staging API deployment on GAE from tempdir: ${TMPDIR}"

  WORKSPACE="${WORKSPACE:-$(upsearch WORKSPACE)}"
  DEPLOY_DIR=${WORKSPACE}/inquiry/tools/deploy

  export TEMP_FILE="${TMPDIR}/app.yaml"

  export_service_name_id

  < "$CONFIG" sed -E "s/SERVICE-NAME/${ENDPOINTS_SERVICE_NAME}/g" \
    | sed -E "s/SERVICE-CONFIG-ID/${ENDPOINTS_SERVICE_CONFIG_ID}/g" \
    > "${TEMP_FILE}"

  echo "${TEMP_FILE}"

  cp ${DEPLOY_DIR}/Dockerfile ${TMPDIR}/
  cp ${DEPLOY_DIR}/configs/dev-requirements.txt ${TMPDIR}/requirements.txt
  cp -r ${DEPLOY_DIR}/devel/inquiry ${TMPDIR}/

  pushd $TMPDIR
  gcloud app deploy
  popd

  echo $(date) : "=== Finished API deployment (GAE)"

}

cleanup() {
  rm -r "$TMPDIR"
}

# Defaults.
CONFIG="${SCRIPT_DIR}/../configs/api.app_tmpl.yaml"

# Cleanup our temporary files even if our deployment fails.
trap cleanup EXIT

deploy_api_gae "$@"
