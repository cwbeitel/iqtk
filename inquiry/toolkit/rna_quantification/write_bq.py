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
"""A dev pipeline to write data from an expression table file to BigQuery."""

import logging

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.utils.pipeline_options import GoogleCloudOptions
from apache_beam.io.gcp.internal.clients import bigquery
from google.protobuf.json_format import MessageToDict

from inquiry.framework.args import job_runner
from inquiry.toolkit.expression.schemas.expression_table_pb2 import (
    DiffExpressionLevel
)

from inquiry.util.bq import WriteToBigQuery, build_schema

SCHEMA = '[{"name":"id","type":"STRING","mode":"NULLABLE"},{"name":"geneid","type":"STRING","mode":"NULLABLE"},{"name":"gene","type":"STRING","mode":"NULLABLE"},{"name":"locus","type":"STRING","mode":"NULLABLE"},{"name":"sample1","type":"STRING","mode":"NULLABLE"},{"name":"sample2","type":"STRING","mode":"NULLABLE"},{"name":"status","type":"STRING","mode":"NULLABLE"},{"name":"expression1","type":"FLOAT","mode":"NULLABLE"},{"name":"expression2","type":"FLOAT","mode":"NULLABLE"},{"name":"lnFoldChange","type":"FLOAT","mode":"NULLABLE"},{"name":"testStatistic","type":"FLOAT","mode":"NULLABLE"},{"name":"pValue","type":"FLOAT","mode":"NULLABLE"},{"name":"qValue","type":"FLOAT","mode":"NULLABLE"},{"name":"significant","type":"BOOLEAN","mode":"NULLABLE"}]'


class BuildRowFn(beam.DoFn):
    def __init__(self):
        super(BuildRowFn, self).__init__()

    def process(self, element):

        row = element.split('\t')

        d = MessageToDict(DiffExpressionLevel(
            id=str(row[0]),
            geneid=str(row[1]),
            gene=str(row[2]),
            locus=str(row[3]),
            sample1=str(row[4]),
            sample2=str(row[5]),
            status=str(row[6]),
            expression1=float(row[7]),
            expression2=float(row[8]),
            lnFoldChange=float(row[9]),
            testStatistic=float(row[10]),
            pValue=float(row[11]),
            qValue=float(row[12]),
            significant=(row[13] == 'yes')
            ), False)

        yield d


class WriteDiffExpressionToBigQuery(WriteToBigQuery):

    def __init__(self, *args, **kwargs):
        super(WriteDiffExpressionToBigQuery, self).__init__(schema=build_schema(SCHEMA),
                                                            *args, **kwargs)

    def row_fn(self, pcoll):
        return (pcoll | 'ConvertToRow' >> beam.ParDo(BuildRowFn()))


def run_bq_write(args, p):

    filename = 'gs://cflow-runs/output/qexpression-20170403103314/cuffdiff-20170403175527/gene_exp.diff'
    table_name = 'sometable4'

    (p
     | ReadFromText(filename, skip_header_lines=1)
     | WriteDiffExpressionToBigQuery(table_name=table_name))


def run(config=None):
    """Run the workflow."""
    job_runner(run_bq_write, job_tag='bq_write', bucket='inquiry-dev',
               arg_template={}, config=config)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
