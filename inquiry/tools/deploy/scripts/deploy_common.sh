#!/bin/bash
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

die() {
  # Print a message and exit with code 1.
  #
  # Usage: die <error_message>
  #   e.g., die "Something bad happened."

  echo $@
  exit 1
}

upsearch () {
  test / == "$PWD" && return || \
      test -e "$1" && echo "$PWD" && return || \
      cd .. && upsearch "$1"
}

get_latest_config_id() {
  # Given a service name, this returns the most recent deployment of that
  # API.
  service_name="$1"
  gcloud service-management configs list \
    --service="$service_name" \
    --sort-by="~config_id" --limit=1 --format="value(CONFIG_ID)" \
    | tr -d '[:space:]'
}

get_project_id() {
  # Find the project ID first by DEVSHELL_PROJECT_ID (in Cloud Shell)
  # and then by querying the gcloud default project.
  local project="${DEVSHELL_PROJECT_ID:-}"
  if [[ -z "$project" ]]; then
    project=$(gcloud config get-value project 2> /dev/null)
  fi
  if [[ -z "$project" ]]; then
    >&2 echo "No default project was found, and DEVSHELL_PROJECT_ID is not set."
    >&2 echo "Please use the Cloud Shell or set your default project by typing:"
    >&2 echo "gcloud config set project YOUR-PROJECT-NAME"
  fi
  echo "$project"
}

export_service_name_id() {
  echo "Obtaining endpoints service name and config id..."
  # Get the name and id of the Endpoints service
  local PROJECT_ID=$(get_project_id)
  if [[ -z "${PROJECT_ID}" ]]; then
    exit 1
  fi
  export ENDPOINTS_SERVICE_CONFIG_ID=`gcloud service-management configs list --service=iqtk-api.endpoints.${PROJECT_ID}.cloud.goog | cut -f1 -d' ' | grep -v CONFIG | head -n1`
  export ENDPOINTS_SERVICE_NAME=`gcloud service-management configs list --service=iqtk-api.endpoints.${PROJECT_ID}.cloud.goog | cut -f3 -d' ' | grep cloud.goog | head -n1`
  #export ENDPOINTS_SERVICE_CONFIG_ID=`gcloud service-management configs list --service=iqtk-api.endpoints.${PROJECT_ID}.cloud.goog | cut -f1 -d' ' | grep -v CONFIG | head -n1`
  #export ENDPOINTS_SERVICE_NAME=`gcloud service-management configs list --service=iqtk-api.endpoints.${PROJECT_ID}.cloud.goog | cut -f3 -d' ' | grep cloud.goog | head -n1`
  echo name: ${ENDPOINTS_SERVICE_NAME}
  echo config_id: ${ENDPOINTS_SERVICE_CONFIG_ID}
}

ensure_kube_cluster_exists() {
  CLUSTER_NAME=inquiry
  DEPLOYMENT=`gcloud container clusters list --filter=name=${CLUSTER_NAME}`
  if [ -z "${DEPLOYMENT}" ]; then
    echo 'Container engine deployment with name ${CLUSTER_NAME} not found, deploying...'
  	gcloud container clusters create ${CLUSTER_NAME} \
  		--scopes "cloud-platform" \
  		--num-nodes 4
  else
    echo 'A container engine deployment named ${CLUSTER_NAME} was found, using that.'
  fi
  gcloud container clusters get-credentials ${CLUSTER_NAME}
}
