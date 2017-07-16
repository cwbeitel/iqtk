# Metagenome Analysis

(Work in progress) This workflow concerns metabolome analysis in the context of obtaining a set of mass distribution vectors for subsequent Flux Balance Analysis (FBA).

## Running `msconvert` to convert Agilent .d files to mzML

We provide a public docker image hosted on the Google Container Registry that extends others (CITE!) previous work to containerize this windows tool so that it runs in Docker's necessarily Linux parent environment. To do this the input data must be present on a volume that is mapped to the file space of the docker container. See [this](https://docs.docker.com/engine/tutorials/dockervolumes/) for details.

```bash
docker run -v [host volume]:[docker volume] gcr.io/jbei-cloud/msconvert:0.0.1 \
    wine msconvert [decompression target in docker volume] \
    --zlib -o [output path on docker volume]
```

## Processing with XCMS3

The workflow for processing raw mzML data into mass distribution vectors is currently available to run as a Jupyter notebook (running an R kernel), check it out [here](inquiry/docs/tutorials/analyze-metabolite-mdvs-xcms3.ipynb). Here we use XCMS3 to perform the analysis and this analysis is an adaptation of a [workflow tutorial](https://bioconductor.org/packages/release/bioc/vignettes/xcms/inst/doc/new_functionality.html) provided as part of the XCMS3 documentation. Alternatively refer [here](https://www.youtube.com/watch?v=SJheOIuWH98) for a tutorial of XCMS Online.

(TODO: Describe parameterization of batch XCMS3 workflow running under standard iqtk framework.)

Operation of the notebook currently requires familiarity with R and basic programming so consult [some](https://www.datacamp.com/) [of](http://tryr.codeschool.com/) [these](https://www.coursera.org/learn/r-programming) resources if you need a refresher.

## Contributing

We'd love you to contribute to the project. Please see our [Contributor guide](../../../CONTRIBUTING.md) to get started.

## License

© Regents of the University of California, 2017. Licensed under an [BSD-3](../../../LICENSE) license.
