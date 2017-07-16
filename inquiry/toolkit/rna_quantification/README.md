# Expression analysis with Tuxedo suite

Given transcriptome sequencing reads, quantifies the abundance of a range of transcripts - either from a static reference set or extending a reference set with newly assembled transcripts in the current sample.

## Usage

An expression analysis run can be initiated with the following command:

```bash
iq run expression --config=path/to/your/run_conf.json
```

Once initiated, jobs can be monitored from the [DataFlow job monitoring interface](https://cloud.google.com/dataflow/pipelines/dataflow-monitoring-intf).

## Configuration

An expression analysis should be parameterized according to the following schema:

```json
{
    "ref_fasta": "gs://path/to/file.fa",
    "genes_gtf": "gs://path/to/file.gtf",
    "cond_a_pairs": [
      ["gs://path/to/file_a1_f.fq", "gs://path/to/file_a1_r.fq"],
      ["gs://path/to/file_a2_f.fq", "gs://path/to/file_a2_r.fq"],
      ...
    ],
    "cond_b_pairs": [
      ["gs://path/to/file_b1_f.fq", "gs://path/to/file_b1_r.fq"],
      ...
    ],
}
```

The following is a functioning example that draws data from a public bucket:

```json
{
  "_meta": {
    "workflow": "core:expression"
  },
  "ref_fasta": "gs://cflow-public/data/genomes/Drosophila_melanogaster/Ensembl/BDGP5.25/Sequence/BowtieIndex/genome.fa",
  "genes_gtf": "gs://cflow-public/data/genomes/Drosophila_melanogaster/Ensembl/BDGP5.25/Annotation/Archives/archive-2015-07-17-14-30-26/Genes/genes.gtf",
  "cond_a_pairs": [
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794483_C1_R1_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794483_C1_R1_2_small.fq"],
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794484_C1_R2_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794484_C1_R2_2_small.fq"],
    ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794485_C1_R3_1_small.fq",
     "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794485_C1_R3_2_small.fq"]
   ],
   "cond_b_pairs": [
     ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794486_C2_R1_1_small.fq",
      "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794486_C2_R1_2_small.fq"],
     ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794487_C2_R2_1_small.fq",
      "gs://cflow-public/data/rnaseq/downsampled_reads/GSM794487_C2_R2_2_small.fq"],
     ["gs://cflow-public/data/rnaseq/downsampled_reads/GSM794488_C2_R3_1_small.fq",
      "gs://cflow-public/data/rnaseq/downsampled_readsGSM794488_C2_R3_2_small.fq"]
    ]
}

```

Paths for input data can be determined by browsing for data within [Google Cloud Storage](https://console.cloud.google.com/storage/). If you data is not yet uploaded to GCS there are [multiple options available](https://cloud.google.com/storage/docs/object-basics).

## Contributing

We'd love you to contribute to the project. Please see our [Contributor guide](../../../CONTRIBUTING.md) to get started.

## License

© Regents of the University of California, 2017. Licensed under an [BSD-3](../../../LICENSE) license.
