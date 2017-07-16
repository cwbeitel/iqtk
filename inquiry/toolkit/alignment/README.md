
# Sequence alignment with BWA MEM

Given a a set of sequence reads and a reference sequence, performs sequence alignment of reads against the reference using the BWA MEM short read alignment algorithm.

## Usage

A sequence alignment run can be initiated with the following command:

```bash
iq run alignment --config=path/to/your/run_conf.json
```

Once initiated, jobs can be monitored from the [DataFlow job monitoring interface](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf).

## Configuration

A sequence alignment run should be parameterized according to the following schema:

```json
{
    "ref_fasta": "gs://path/to/file.fa",
    "read_pairs": [
      "gs://path/to/file_a1_f.fq",
      "gs://path/to/file_a1_r.fq",
      ...
    ],
}
```

The following is a functioning example that draws data from a public bucket:

```json
{
  "_meta": {
    "workflow": "core:align"
  },
  "ref_fasta": "gs://cflow-public/data/genomes/Drosophila_melanogaster/Ensembl/BDGP5.25/Sequence/BowtieIndex/genome.fa",
  "read_pairs": [
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794483_C1_R1_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794483_C1_R1_2_small.fq"],
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794484_C1_R2_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794484_C1_R2_2_small.fq"],
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794485_C1_R3_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794485_C1_R3_2_small.fq"]
   ]
}
```

Paths for input data can be determined by browsing for data within [Google Cloud Storage](https://console.cloud.google.com/storage/). If you data is not yet uploaded to GCS there are [multiple options available](https://cloud.google.com/storage/docs/object-basics).

## Contributing

We'd love you to contribute to the project. Please see our [Contributor guide](../../../CONTRIBUTING.md) to get started.

## License

© Regents of the University of California, 2017. Licensed under an [BSD-3](../../../LICENSE) license.
