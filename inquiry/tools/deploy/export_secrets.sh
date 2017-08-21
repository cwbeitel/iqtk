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

# jbei-cloud
# export IQTK_API_KEY=AIzaSyCnvan1G9nDwa1dTRWYQ1EIKTW3tRVyXYI
# export IQTK_OAUTH_CLIENT_ID="1066838427803-mj1p4rf5meot88lb0mq6hbehnqkd3ejt"
# export IQTK_CLIENT_SECRETS_FILE=${SCRIPT_DIR}/configs/oauth2_client_secrets.jbei-cloud.json

# ml-beam
export IQTK_DEPLOY_PROJECT_ID=ml-beam
export IQTK_API_KEY=AIzaSyBay9oww13cgJ83HMImWt7Y0vwd8ATHgVc
export IQTK_OAUTH_CLIENT_ID=523455313934-u3odek2cve1g3m55g5s3v2pmas2kf5r5
export IQTK_CLIENT_SECRETS_FILE=/Users/cb/Desktop/release/iqtk/inquiry/tools/deploy/configs/oauth2_client_secrets.ml-beam.json
export LOCAL_SA_KEY_JSON=/Users/cb/Desktop/release/iqtk/inquiry/tools/deploy/configs/sa-key.json
#export IQTK_SERVICE_ACCOUNT_PROJECT_ID=$(cat ${IQTK_SERVICE_ACCOUNT_KEY_FILE} | grep project_id | cut -f4 -d' ' | sed 's/"//g' | sed 's/,//g')
