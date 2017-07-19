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

# requires BUILD_TAG from environment, e.g.
# BUILD_TAG=iqtk:0.0.1; sh inquiry/tools/ci_build/builds/build_release_container.sh
# requires image iqtk-base exists

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/builds_common.sh"

if [ -z "${QUAY_IO_IQTK_UNAME}" ]; then
  die 'Quay.io username must be defined via. \$QUAY_IO_IQTK_UNAME.'
fi

if [ -z "${QUAY_IO_IQTK_PASSWORD}" ]; then
  die 'Quay.io password must be defined via. \$QUAY_IO_IQTK_PASSWORD.'
fi

if [[ -z "${BUILD_TAG}" ]]; then
  die "The variable BUILD_TAG must be defined before building release container."
fi

docker login -u ${QUAY_IO_IQTK_UNAME} -p ${QUAY_IO_IQTK_PASSWORD} quay.io

docker tag ${BUILD_TAG} quay.io/iqtk/${BUILD_TAG}

docker push quay.io/iqtk/${BUILD_TAG}
