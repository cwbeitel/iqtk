<div align="center">
  <img src="inquiry/docs/assets/logotype_blue_small.png" style="width:100px"></img>
</div>

-----------------
| **`Build Status`** | **`Quality`** | **`Container`** |
|----------------|-----------------|-----------------|
|[![CircleCI](https://circleci.com/gh/iqtk/iqtk.svg?style=svg)](https://circleci.com/gh/iqtk/iqtk)|[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4dc4988373ec4b678279bed718321fcc)](https://www.codacy.com/app/chris-w-beitel/iqtk?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=iqtk/iqtk&amp;utm_campaign=Badge_Grade)|[![Docker Repository on Quay](https://quay.io/repository/iqtk/iqtk/status "Docker Repository on Quay")](https://quay.io/repository/iqtk/iqtk)|

**We use [GitHub issues](https://github.com/iqtk/iqtk/issues) for
tracking requests and bugs.**

**This project is currently pre-alpha and should probably not yet be used in production without support.**

### Check out the full documentation at <b><a href="http://iqtk.io">iqtk.io</a></b>

Watch the [July status update / technical demonstration screencast](https://www.youtube.com/embed/gzB6Cba8u9E).

## Getting started

Here are a few tutorials to get you started!

* [Genotype Analysis with Samtools:](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/tutorials/genotype-samtools.ipynb) Learn how to call genome sequence polymorphisms against a reference genome sequence.
* [Metabolome analysis with XCMS3:](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/tutorials/metabolite-analysis.ipynb) Learn how to use XCMS3 to quantify the levels of metabolites in a sample of interest.
* [Transcriptome analysis with the Tuxedo suite:](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/tutorials/rna_quantification.ipynb) Learn how to quantify and compare gene expression levels across samples.

Each of the above tutorials shows you how to submit workflows form the `iqtk` command line utility as well as how to retrieve the resulting data from BigQuery into a form suitable for exploratory analysis and visualization.

# Developers

## Running workflows from the command line

In addition to the above, workflow runs can be initiated from the command line allowing among other things programmatic integration with other parts of an organization's infrastructure.

### Setup

For this purpose, the toolkit can be installed (which we suggest doing within a virtual environment like `conda` or `virtualenv`) with the following command.

```bash
pip install iqtk
```

Alternatively, the latest `iqtk` docker image can be obtained as follows:

```bash
docker pull quay.io/iqtk/iqtk
```

### GCloud authentication

The environment in which the toolkit is running must have been authenticated to a google cloud account and project (using `gcloud auth login`) that has the Google Genomics Pipelines and DataFlow API's enabled. Also, for the time being you must manually create a bucket with the name `gs://[your-project]-iqtk`.

### Running a workflow

The core workflows can be run as simply as the following,

```bash
iqtk run expression --config=[path to your JSON config e.g. ~/diffex.json]
```

provided a config file with the necessary input files. The following is an example of this for the RNA-seq analysis workflow:

```json
# diffex.json
{
  "cloud": true,
  "local": false,
  "ref_fasta": "gs://iqtk/dmel/bt2/genome.fa",
  "genes_gtf": "gs://iqtk/dmel/annotation/genes.gtf",
  "cond_a_pairs": [
      ["gs://iqtk/rnaseq/GSM794483_C1_R1_1_small.fq",
       "gs://iqtk/rnaseq/GSM794483_C1_R1_2_small.fq"]
      ],
  "cond_b_pairs": [
       ["gs://iqtk/rnaseq/GSM794486_C2_R1_1_small.fq",
        "gs://iqtk/rnaseq/GSM794486_C2_R1_2_small.fq"]
       ]
}

```

## Developing workflows

New workflows can be developed in an environment where `iqtk` has been pip installed by, at the top level, subclassing the core `iqtk.Workflow` object along with making use of the core `util.fc_create`, `util.match`, and `util.combine` operations to express how file objects resulting from an operation should be mapped to a downstream operation.

### Writing a workflow

To illustrate the structure (and hopefully simplicity) of building new workflows, per one of the core objectives of the project, the following example (a simplified version of the full RNA-seq workflow) is provided. As you can see a `Workflow` subclass `define` method specifies a mapping of input and intermediate file collections through a series of operations, providing a file property query syntax to express abstract notions of workflow structure (e.g. "the files that should be processed by cufflinks are all of the files of type bam produced from the alignment steps").

```python

class TranscriptomicsWorkflow(Workflow):
    def __init__(self):
        """Initialize a workflow."""
        self.tag = 'tuxedo-transcriptomics'
        self.arg_template = [details omitted]
        super(TranscriptomicsWorkflow, self).__init__()

    def define(self):
        p, args = self.p, self.args

        # # For each condition, create a PCollection to store the input read pairs.
        reads_a = util.fc_create(p, args.cond_a_pairs)
        reads_b = util.fc_create(p, args.cond_b_pairs)

        # For each pair of reads, use tophat to perform split-read alignment.
        # Condition A.
        th_a = (reads_a | task.ContainerTaskRunner(
            ops.TopHat(args=args,
                       ref_fasta=args.ref_fasta,
                       genes_gtf=args.genes_gtf,
                       tag='cond_a')
            ))

        th_b = (reads_b | task.ContainerTaskRunner(
            ops.TopHat(args=args,
                       ref_fasta=args.ref_fasta,
                       genes_gtf=args.genes_gtf,
                       tag='cond_b')
            ))

        # Subset the outputs of the tophat steps to obtain only the bam (alignment)
        # files. Then combine the collections.
        align_a = util.match(th_a, {'file_type': 'bam'})
        align_b = util.match(th_b, {'file_type': 'bam'})
        align = util.combine(p, (align_a, align_b))

        # For each set of reads, perform a transcriptome assembly with cufflinks,
        # yielding one gtf feature annotation for each input read set.
        cl = (align | task.ContainerTaskRunner(
            ops.Cufflinks(args=args)
            ))

        # Perform a single `cuffmerge` operation to merge all of the gene
        # annotations into a single annotation.
        cm = (util.union(util.match(cl, {'file_type': 'transcripts.gtf'}))
              | task.ContainerTaskRunner(
                  ops.CuffMerge(args=args,
                                ref_fasta=args.ref_fasta,
                                genes_gtf=args.genes_gtf)
                  ))

        # Run a single cuffdiff operation comparing the prevalence of features in
        # the input annotatio across conditions using reads obtained for those
        # conditions.
        cd = ops.cuffdiff(util.match(cm, {'file_type': 'gtf'}),
                          ref_fasta=args.ref_fasta,
                          args=args,
                          cond_a_bams=AsList(align_a),
                          cond_b_bams=AsList(align_b))

        return cd

```

Instances of `ContainerTask`, such as `TopHat`, can easily be shared among a community of developers and remixed to quickly prototype new workflows. The following simple example illustrates how developers can subclass `ContainerTask` to create new containerized operations.

```python
class TopHat(task.ContainerTask):

    def __init__(self, args, tag=None):
        container = task.ContainerTaskResources(
            disk=60, cpu_cores=4, ram=8,
            image='gcr.io/jbei-cloud/tophat:0.0.1')
        super(TopHat, self).__init__(task_label='dummy', args=args,
                                     container=container)

    def process(self, input_file):

        cmd = util.Command(['cat', localize(input_file), '>',
                            self.out_path + '/file.txt'])

        yield self.submit(cmd.txt, inputs=[input_file],
                          expected_outputs=[{'txt': 'file.txt'}])
```

Here one can see that the platform and environment in which a task runs is abstracted permitting it to be parameterized at runtime and simplifying the operational considerations for workflow developers.

For more detailed examples of workflows and operations check out any of those provided as part of the core toolkit, e.g. [the one for RNA-seq analysis](https://github.com/iqtk/iqtk/blob/master/inquiry/toolkit/rna_quantification/workflow.py).

### Data schema

A key objective of the project has been to provide consistent delivery of the data resulting from workflow runs to databases according to a controlled and standardized schemas. Significant effort on the part of the Global Alliance for Genomics and Health (GA4GH) is underway in this area. Here we make use of lightly adapted versions of [those schemas](https://github.com/ga4gh/ga4gh-schemas/tree/master/src/main/proto/ga4gh).

For more details you can [browse an example schema](https://github.com/iqtk/iqtk/blob/master/inquiry/protobuf/inquiry/toolkit/rna_quantification/schemas/rna_quantification.proto) or check out a [BigQuery table](https://bigquery.cloud.google.com/table/jbei-cloud:somedataset.sometable2?tab=preview) with RNA-seq data using this schema.

#### Acknowledgments

© Regents of the University of California, 2017. Licensed under a BSD-3 <a href="https://github.com/.../blob/master/LICENSE">license</a>.

Thank you to those who have made this project possible. Read more in our [acknowledgments of support](https://github.com/iqtk/iqtk/tree/master/inquiry/docs/support.md).
