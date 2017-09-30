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


# Deploy or update the run route
if [[ -z "$(fission function get --name run)" ]]; then
  fission function create --name run --env python --code ${SCRIPT_DIR}/run.py
else
  fission function update --name run --env python --code ${SCRIPT_DIR}/run.py
fi

# Deploy or update the list route
if [[ -z "$(fission function get --name list)" ]]; then
  fission function create --name list --env python --code ${SCRIPT_DIR}/list.py
else
  fission function update --name list --env python --code ${SCRIPT_DIR}/list.py
fi

# Deploy or update the describe route
if [[ -z "$(fission function get --name describe)" ]]; then
  fission function create --name describe --env python --code ${SCRIPT_DIR}/describe.py
else
  fission function update --name describe --env python --code ${SCRIPT_DIR}/describe.py
fi

# Deploy or update the health route
if [[ -z "$(fission function get --name health)" ]]; then
  fission function create --name health --env python --code ${SCRIPT_DIR}/health.py
else
  fission function update --name health --env python --code ${SCRIPT_DIR}/health.py
fi


# TODO: So here it would be good if we either created a new route or if already
# exists its updated in the right way.

fission route create --method POST --url /run --function run
fission route create --method POST --url /list --function list
fission route create --method POST --url /describe --function describe
fission route create --method GET --url /health --function health
