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
CONFIGS_DIR=$(cd ${SCRIPT_DIR}/../configs && pwd)

if ! [ -z ${CURRENT_IQTK_DEVEL_IMAGE_TAG} ]; then
  die 'before a local dev container can be started we need to have built one. define its tag with CURRENT_IQTK_DEVEL_IMAGE_TAG'
fi

start_local_dev_container() {
  echo "for local development, set ENDPOINTS_HOST=localhost:8080"
  echo "starting container..."
  docker run -p 127.0.0.1:8080:8080 \
    -v ${CONFIGS_DIR}:/key \
    -e "GOOGLE_APPLICATION_CREDENTIALS=/key/sa-key.json" \
    -it ${CURRENT_IQTK_DEVEL_IMAGE_TAG} /bin/bash
}

main "$@"
