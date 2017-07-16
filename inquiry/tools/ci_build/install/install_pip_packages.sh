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

# We don't apt-get install so that we can install a newer version of pip. Not
# needed after we upgrade to Ubuntu 16.04
easy_install -U pip
easy_install3 -U pip

# Install pip packages from whl files to avoid the time-consuming process of
# building from source.
pip2 install wheel
pip3 install wheel

# Install six.
pip2 install --upgrade six==1.10.0
pip3 install --upgrade six==1.10.0
