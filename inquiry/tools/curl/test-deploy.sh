#!/bin/sh
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
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

die() {
  echo $@
  exit 1
}

curl -fsSL scripts.iqtk.io/setup -o ${SCRIPT_DIR}/setup

if ! [[ "cmp --silent ${SCRIPT_DIR}/setup ${SCRIPT_DIR}/public/setup" ]]; then
  die "Setup script pulled does not match local."
fi

if ! [[ "docker run -it gcr.io/jbei-cloud/iqtk:latest iqtk checkup" ]]; then
  # TODO: Doesn't work currently but you get the general idea
  die "Docker image obtained from gcr.io/jbei-cloud/iqtk:latest could not load iqtk."
fi

rm ${SCRIPT_DIR}/setup
