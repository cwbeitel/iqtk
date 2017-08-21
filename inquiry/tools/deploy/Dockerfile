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

# FROM gcr.io/google_appengine/python
FROM iqtk-base:latest

# RUN apt-get update && \
#    apt-get install -y python2.7 python-pip && \
#    apt-get clean && \
#    rm /var/lib/apt/lists/*_*

ADD . /app
WORKDIR /app

RUN pip2 install /app/iqtk-*-py2-none-any.whl
# RUN pip2 install /app/iqtk*.tar.gz
# RUN pip install -r requirements.txt

# Works fine, could use for mixture of iqtk/non-iqtk services.
# CMD honcho start -f /app/procfile $PROCESSES

CMD iq-serv --service=$PROCESSES
