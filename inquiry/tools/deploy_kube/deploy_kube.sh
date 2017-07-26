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

CLUSTER_NAME=inquiry

DEPLOYMENT=`gcloud container clusters list --filter=name=${CLUSTER_NAME}`
if [ -z "${DEPLOYMENT}" ]; then
	gcloud container clusters create ${CLUSTER_NAME} \
		--scopes "cloud-platform" \
		--num-nodes 4
fi

gcloud container clusters get-credentials ${CLUSTER_NAME}

kubectl delete all -l app=iqtk
kubectl create -f inquiry/tools/deploy_kube/configs/iqtk.yaml --validate=false
