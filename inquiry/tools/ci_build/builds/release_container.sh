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
DOCKERFILE_PATH="${SCRIPT_DIR}/Dockerfile.deploy"
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
BUILD_TAG="${BUILD_TAG:-base}"

# Determine the docker image name
DOCKER_IMG_NAME="${BUILD_TAG}"

# Under Jenkins matrix build, the build tag may contain characters such as
# commas (,) and equal signs (=), which are not valid inside docker image names.
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | sed -e 's/=/_/g' -e 's/,/-/g')

# Convert to all lower-case, as per requirement of Docker image names
DOCKER_IMG_NAME=$(echo "${DOCKER_IMG_NAME}" | tr '[:upper:]' '[:lower:]')
export DOCKER_IMG_NAME=${DOCKER_IMG_NAME}

# Print arguments.
echo "WORKSPACE: ${WORKSPACE}"
echo "COMMAND: ${COMMAND[@]}"
echo "BUILD_TAG: ${BUILD_TAG}"
echo "  (docker container name will be ${DOCKER_IMG_NAME})"
echo ""

# Build the docker container.
echo "Building container (${DOCKER_IMG_NAME})..."
docker build -t ${DOCKER_IMG_NAME} \
    -f "${DOCKERFILE_PATH}" "${WORKSPACE}"
