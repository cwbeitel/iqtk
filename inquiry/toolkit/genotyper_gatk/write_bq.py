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
"""Variant write to BQ."""

import logging
import apache_beam as beam

from apache_beam.io import ReadFromText
from google.protobuf.json_format import MessageToDict

from inquiry.framework.args import job_runner
from inquiry.util.bq import WriteToBigQuery, build_schema
from inquiry.toolkit.genotyping.schemas.genotype_pb2 import (
    Variant
)

SCHEMA = '[{"name":"id","type":"STRING","mode":"NULLABLE"},{"name":"refname","type":"STRING","mode":"NULLABLE"},{"name":"start","type":"INTEGER","mode":"NULLABLE"},{"name":"end","type":"INTEGER","mode":"NULLABLE"},{"name":"refbases","type":"STRING","mode":"NULLABLE"},{"name":"altbases","type":"STRING","mode":"REPEATED"},{"name":"quality","type":"FLOAT","mode":"NULLABLE"},{"name":"filter","type":"STRING","mode":"NULLABLE"},{"name":"info","type":"STRING","mode":"NULLABLE"},{"name":"format","type":"STRING","mode":"NULLABLE"}]'


class BuildRowFn(beam.DoFn):
    def __init__(self):
        super(BuildRowFn, self).__init__()

    def process(self, element):

        row = element.split('\t')

        d = MessageToDict(Variant(
            id=str(row[2]),
            refname=str(row[0]),
            start=int(row[1]),
            refbases=str(row[3]),
            altbases=str(row[4]),
            quality=float(row[5]),
            filter=str(row[6]),
            info=str(row[7]),
            format=str(row[8])
            ), False)

        yield d


class WriteVariantsToBigQuery(WriteToBigQuery):

    def __init__(self, *args, **kwargs):
        super(WriteVariantsToBigQuery, self).__init__(schema=build_schema(SCHEMA),
                                                      *args, **kwargs)

    def row_fn(self, pcoll):
        return (pcoll | 'ConvertToRow' >> beam.ParDo(BuildRowFn()))


def run_bq_write(args, p):

    filename = 'gs://inquiry-test/output/test-e2e-0-20170428070609/samtools_mpileup-20170428070610/var.flt.vcf.body'
    table_name = 'variants3'

    (p
     | ReadFromText(filename, skip_header_lines=1)
     | WriteVariantsToBigQuery(table_name=table_name))


def run(config=None):
    """Run the workflow."""
    job_runner(run_bq_write, job_tag='bq_write', bucket='inquiry-dev',
               arg_template={}, config=config)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
