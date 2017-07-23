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
"""Genotype analysis pipeline."""

from __future__ import absolute_import

from . import operations as ops
from inquiry.framework.workflow import Workflow
from inquiry.framework import util
from inquiry.framework import task


class GenotypeGATKWorkflow(Workflow):

    def __init__(self):
        """Initialize the workflow."""
        self.tag = 'genotype-gatk'
        self.arg_template = {
            "ref_fasta": {
                "help": "The reference genome assembly."
            },
            "reads": {
                "help": "An array of read pairs to use in the genotype analysis"
            }
        }
        self.meta = {
          "name": "genotype-gatk",
          "description": "Call genotypes using the GATK best practices pipeline.",
          "parameters": [{
            "name": "ref_fasta",
            "label": "Reference FASTA",
            "help_text": "GCS path to reference genome assembly in FASTA format (aginst which to align reads).",
            "regexes": ["^gs:\/\/[^\n\r]+$"],
            "is_optional": False
          },
          {
            "name": "reads",
            "label": "Reads FASTQ's",
            "help_text": "GCS path to file listing input reads.",
            "regexes": ["^gs:\/\/[^\n\r]+$"],
            "is_optional": False
          }]
        }
        super(GenotypeGATKWorkflow, self).__init__()

    def define(self):
        return (util.fc_create(self.p, self.args.reads)
                | task.ContainerTaskRunner(
                    ops.CombinedSamtoolsGenotyper(
                        self.args,
                        self.args.ref_fasta
                        )))

        reads = util.fc_create(self.p, self.args.reads)
        return ops.genotype(reads, self.args)

# class GenotypeGATKWorkflow(Workflow):
#
#     def __init__(self):
#         """Initialize the workflow."""
#         self.meta = {
#           "name": "genotype-gatk",
#           "description": "Call genotypes using the GATK best practices pipeline.",
#           "parameters": [{
#             "name": "ref_fasta",
#             "label": "Reference FASTA",
#             "help_text": "GCS path to reference genome assembly in FASTA format.",
#             "regexes": ["^gs:\/\/[^\n\r]+$"],
#             "is_optional": False
#           },
#           {
#             "name": "reads",
#             "label": "Reads FASTQ's",
#             "help_text": "GCS path to file listing input reads.",
#             "regexes": ["^gs:\/\/[^\n\r]+$"],
#             "is_optional": False
#           }]
#         }
#         super(GenotypeGATKWorkflow, self).__init__()
#
#     def define(self):
#         aligned = (util.fc_create(self.p, self.args.reads)
#                    | task.ContainerTaskRunner(
#                        ops.BWAMem(
#                            self.args,
#                            self.args.ref_fasta,
#                            mark_duplicates = True,
#                            generate_bam = True
#                            )
#                        ))
#
#         indel_realigned = (fc_match(aligned, {'file_type': 'deduped.bam'})
#                            | task.ContainerTaskRunner(
#                                ops.IndelRealignment(
#                                    self.args,
#                                    self.args.ref_fasta
#                                    )
#                                ))
#
#         recalibrated = (fc_match(indel_realigned, {'file_type': 'bam'})
#                         | task.ContainerTaskRunner(
#                             ops.BaseQualityRecalibrate(
#                                 self.args,
#                                 self.args.ref_fasta
#                                 )
#                             ))
#
#         raw_calls = (fc_match(recalibrated, {'file_type': 'bam'})
#                      | task.ContainerTaskRunner(
#                          ops.HaploypeCaller(
#                              self.args,
#                              self.args.ref_fasta
#                              )
#                          ))
#
#         recal_calls = (fc_match(raw_calls, {'file_type': 'bam'})
#                        | task.ContainerTaskRunner(
#                            ops.VQSR(
#                                self.args,
#                                self.args.ref_fasta
#                                )
#                            ))
#
#         return recal_calls

def run(config=None):
    """Run as a Dataflow."""
    GenotypeGATKWorkflow().run(config)

if __name__ == '__main__':
    run(sys.argv[1])
