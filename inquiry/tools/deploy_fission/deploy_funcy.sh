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

export FISSION_URL=http://$(kubectl --namespace fission get svc controller -o=jsonpath='{..ip}')
export FISSION_ROUTER=$(kubectl --namespace fission get svc router -o=jsonpath='{..ip}')

# Create the function and delete previous first if necessary
if [[ "$(fission \function list | grep ${FUNC_NAME})" ]]; then
  fission \function delete --name ${FUNC_NAME}
fi
fission function create --name ${FUNC_NAME} --env ${ENV_NAME} --code ${FUNC_NAME}.py

# Create the route and delete the previous if necessary
# TODO: So this will delete /func in addition to /funcy ...
if [[ "$(fission route list | cut -f6 -d' ' | grep /${FUNC_ROUTE})" ]]; then
  ROUTE_NAME=`fission route list | grep /${FUNC_ROUTE} | cut -f1 -d' '`
  fission route delete --name ${ROUTE_NAME}
fi

fission route create --method GET --url /${FUNC_ROUTE} --function ${FUNC_NAME}

# Test the route
echo testing route http://${FISSION_ROUTER}/${FUNC_ROUTE}
curl http://${FISSION_ROUTER}/${FUNC_ROUTE}
