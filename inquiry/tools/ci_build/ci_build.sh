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

# Dockerfile to be used in docker build
DOCKERFILE_PATH="${SCRIPT_DIR}/Dockerfile"
DOCKER_CONTEXT_PATH="${SCRIPT_DIR}"

COMMAND=("$@")

# Helper function to traverse directories up until given file is found.
function upsearch () {
  test / == "$PWD" && return || \
      test -e "$1" && echo "$PWD" && return || \
      cd .. && upsearch "$1"
}

# Set up WORKSPACE and BUILD_TAG. Jenkins will set them for you or we pick
# reasonable defaults if you run it outside of Jenkins.
WORKSPACE="${WORKSPACE:-$(upsearch WORKSPACE)}"

BASE_BUILD_TAG="${BUILD_TAG:-base}"

# Determine the docker image name
DOCKER_IMG_NAME="${BASE_BUILD_TAG}"

# Under Jenkins matrix build, the build tag may contain characters such as
# commas (,) and equal signs (=), which are not valid inside docker image names.
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | sed -e 's/=/_/g' -e 's/,/-/g')

# Convert to all lower-case, as per requirement of Docker image names
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | tr '[:upper:]' '[:lower:]')
export DOCKER_IMG_NAME=${DOCKER_IMG_NAME}

# Print arguments.
echo "WORKSPACE: ${WORKSPACE}"
echo "COMMAND: ${COMMAND[@]}"
echo "BASE_BUILD_TAG: ${BASE_BUILD_TAG}"
echo "  (docker container name will be ${DOCKER_IMG_NAME})"
echo ""

# Build the docker container.
echo "Building container (${DOCKER_IMG_NAME})..."
docker build -t ${DOCKER_IMG_NAME} \
    -f "${DOCKERFILE_PATH}" "${DOCKER_CONTEXT_PATH}"

# Check docker build status
if [[ $? != "0" ]]; then
  die "ERROR: docker build failed. Dockerfile is at ${DOCKERFILE_PATH}"
fi

# Run the command inside the container.
echo "Running '${COMMAND[@]}' inside docker image named ${DOCKER_IMG_NAME}..."
#export HOST_CACHE_DIR=${WORKSPACE}/bazel-ci_build-cache
HOST_CACHE_DIR=${WORKSPACE}/.cache/bazel
mkdir -p ${HOST_CACHE_DIR}
# By default we cleanup - remove the container once it finish running (--rm)
# and share the PID namespace (--pid=host) so the process inside does not have
# pid 1 and SIGKILL is propagated to the process inside (jenkins can kill it).
# --rm
DOCKER_BINARY=`which docker` # hack
DOCKER_COMMAND="${DOCKER_BINARY} run --pid=host \
    -v ${HOST_CACHE_DIR}:/root/.cache/bazel \
    -v ${WORKSPACE}:/workspace \
    -w /workspace \
    ${DOCKER_IMG_NAME} \
    ${COMMAND[@]}"

echo $DOCKER_COMMAND

# Comment out for local development and run container interactively, for now
# Either that or don't run bazel clean...?
${DOCKER_COMMAND}
