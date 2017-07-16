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

project=jbei-cloud
version=0.0.1
tool=aligntools
tag=gcr.io/${project}/${tool}:${version}

#rm ./var*
#rm aln.sam && rm aln.bam

docker build -t ${tag} .

#docker run -t ${tag} sh job.sh

gcloud docker -- push ${tag}
