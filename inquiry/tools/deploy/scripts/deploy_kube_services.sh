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

# TODO: There is complexity to deal with here related to what happens when we want
# to update a production deployment without interrupting running jobs i.e. we'd want
# to let workers finish their current task before updating the image.
# For now this is strictly for an initial deployment or replacing an existing
# deployment after the running tasks have completed.
# One solution that might be necessary anyway is to make the system tolerant to
# job crashes / able to re-start.
# One approach to that would be to have a primary container that receves job
# requests and submits each as its own kubernetes job, only acking the job meg
# if it was submitted successfully.

# TODO: An important thing to note here is that if we build a new image that
# has the same tag as one used in an old deployment it will use the old image
# instead of pulling the new one. Either there should be some logic or docs.
# to prevent this from happening.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/deploy_common.sh"


if [ -z "${IQTK_DEPLOY_VERSION}" ]; then
  die 'The IQTK_DEPLOY_VERSION (e.g. 0.0.1) must be defined before running deploy_kube_services.sh'
fi

function main() {

  # local PROJECT_ID=$(get_project_id)
  # Maybe better to require this be set explictly instead of assumed from
  # current set project given cost of personal/business billing errors.

  if [[ -z "${IQTK_DEPLOY_PROJECT_ID}" ]]; then
    die 'Please define the project ID to be used in the IQTK deployment explicitly via ${IQTK_DEPLOY_PROJECT_ID}'
  fi

  # Template ${IQTK_DEPLOY_TAG} into IQTK-DEPLOY-TAG and
  # ${PROJECT_ID} into IQTK-DEPLOY-PROJECT-ID fields of both
  # flow-runner.kube.yaml and iot-handler.kube.yaml.

  export TMPDIR=$(mktemp -d -t tmp.XXXXXXXXXX)

  echo $(date) : "=== Templating iqtk service deployment configs"

  WORKSPACE="${WORKSPACE:-$(upsearch WORKSPACE)}"
  FLOW_RUNNER_CONFIG=${WORKSPACE}/inquiry/tools/deploy/configs/flow-runner.tmpl.yaml
  IOT_HANDLER_CONFIG=${WORKSPACE}/inquiry/tools/deploy/configs/iot-handler.tmpl.yaml

  < "$FLOW_RUNNER_CONFIG" sed -E "s/IQTK-DEPLOY-IMAGE-VERSION/${IQTK_DEPLOY_VERSION}/g" \
    | sed -E "s/IQTK-DEPLOY-PROJECT-ID/${IQTK_DEPLOY_PROJECT_ID}/g" \
    > "${TMPDIR}/flow-runner.yaml"

  < "$IOT_HANDLER_CONFIG" sed -E "s/IQTK-DEPLOY-IMAGE-VERSION/${IQTK_DEPLOY_VERSION}/g" \
    | sed -E "s/IQTK-DEPLOY-PROJECT-ID/${IQTK_DEPLOY_PROJECT_ID}/g" \
    > "${TMPDIR}/iot-handler.yaml"

  if ! [ -z "$(kubectl get deployments -l service=flow-runner -o json | grep replicas)" ]; then
    kubectl delete deployments iqtk-flow-runner
  fi

  if ! [ -z "$(kubectl get deployments -l service=iot-handler -o json | grep replicas)" ]; then
    kubectl delete deployments iqtk-iot-handler
  fi

  # debug
  cat ${TMPDIR}/flow-runner.yaml
  cat ${TMPDIR}/iot-handler.yaml

  kubectl create -f ${TMPDIR}/flow-runner.yaml --validate=false
  kubectl create -f ${TMPDIR}/iot-handler.yaml --validate=false

  echo $(date) : "=== Deploy complete"

}

cleanup() {
  rm -r "$TMPDIR"
}

# Cleanup our temporary files even if our build fails.
trap cleanup EXIT

main "$@"
