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

if [[ -z "${BUILD_TAG}" ]]; then
  die "The variable BUILD_TAG must be defined before building release container."
fi

if [[ "$(docker images -q iqtk-base:latest 2> /dev/null)" == "" ]]; then
  die "The base iqtk container must have been built before building release."
fi

function upsearch () {
  test / == "$PWD" && return || \
      test -e "$1" && echo "$PWD" && return || \
      cd .. && upsearch "$1"
}

DOCKERFILE_PATH="${SCRIPT_DIR}/../Dockerfile.release"
WORKSPACE="${WORKSPACE:-$(upsearch WORKSPACE)}"

DOCKER_IMG_NAME="${BUILD_TAG}"
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | sed -e 's/=/_/g' -e 's/,/-/g')
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | tr '[:upper:]' '[:lower:]')
export DOCKER_IMG_NAME=${DOCKER_IMG_NAME}

# Print arguments.
echo "WORKSPACE: ${WORKSPACE}"
echo "BUILD_TAG: ${BUILD_TAG}"
echo "  (docker container name will be ${DOCKER_IMG_NAME})"
echo ""

# Copy Dockerfile and whl to tempdir for build...
TMPDIR=$(mktemp -d -t tmp.XXXXXXXXXX)

echo $(date) : "=== Building release container in tmpdir: ${TMPDIR}"

ls ${WORKSPACE}
cp ${DOCKERFILE_PATH} ${TMPDIR}/Dockerfile
cp ${WORKSPACE}/pip_test/whl/* ${TMPDIR}

# DEV
cp ${WORKSPACE}/inquiry/tools/ci_build/install/install_gcloud.sh ${TMPDIR}

pushd ${TMPDIR}
echo $(date) : "=== Building release container"
# Build the docker container.
echo "Building container (${DOCKER_IMG_NAME})..."
docker build -t ${DOCKER_IMG_NAME} \
    -f "${TMPDIR}/Dockerfile" "${TMPDIR}"
popd
rm -rf ${TMPDIR}
