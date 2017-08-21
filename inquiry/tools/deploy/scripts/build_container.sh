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

# Note: The IQTK container will typically be built using the ci_build workflow
# which involves running various stages of test in an organized way before
# finishing the build of a pip whl that can then be either installed in the
# container or deployed to pypi.
# This script is for development purposes - to refactor to have multiple procs
# able to be initiated for same container from a procfile.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/deploy_common.sh"

export DEPLOY_TAG=quay.io/iqtk/iqtk:deploy-devel

function build_container() {

  export TMPDIR=$(mktemp -d -t tmp.XXXXXXXXXX)

  echo $(date) : "=== Building dev container in tmpdir: ${TMPDIR}"

  WORKSPACE="${WORKSPACE:-$(upsearch WORKSPACE)}"
  DEPLOY_DIR=${WORKSPACE}/inquiry/tools/deploy

  cp ${DEPLOY_DIR}/Dockerfile ${TMPDIR}/
  # cp ${DEPLOY_DIR}/configs/dev-requirements.txt ${TMPDIR}/requirements.txt
  # cp -r ${DEPLOY_DIR}/devel/inquiry ${TMPDIR}/
  cp -r ${DEPLOY_DIR}/procfile ${TMPDIR}/
  cp ${WORKSPACE}/pip_test/whl/* ${TMPDIR}/

  pushd $TMPDIR
  docker build -t ${DEPLOY_TAG} .
  popd

  echo $(date) : "=== Build complete"

}

# deploy_container() {
#   docker push ${DEPLOY_TAG}
# }

cleanup() {
  rm -r "$TMPDIR"
}

# Cleanup our temporary files even if our build fails.
trap cleanup EXIT

build_container "$@"
