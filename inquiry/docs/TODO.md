
#### Open

- Establish an extensible framework for analytical workflows that positions for future

  - Not satisfied with use of Apache Beam as core workflow framework. Porting to Fission / serverless, see [design](https://github.com/iqtk/iqtk/blob/master/inquiry/operations/README.md).


#### Hold

- Establish a paradigm for automated triggering of analysis

  - More complicated than we thought and we don’t have the volume for this to be necessary right now. This should be pursued in the context of a broader, more cohesive vision for how devices, generally, interface with the infrastructure that takes signals from them and turns that into structured information.


#### Un-started

- Prototype novel analytical modules
  - Neural base caller
  - Molecular dynamics simulation

#### Closed

- Implement a basic credentialed REST API using cloud endpoints

- Implement an analytical workflow for transcriptome analysis

- Allow workflows to deliver resulting data to a structured data warehouse; demonstrate how to do this according to a controlled and extensible data schema

- Put in place temporary instrument data sync infrastructure

- Be able to test run containerized workflows locally to accelerate development

- Establish project code, test, etc. organization in such a way as to support significant growth in project complexity while maintaining systems integration

  - Testing is progressive given length of time required to do full run of infra


- Implement an analytical workflow for metabolite analysis

  - Currently able to run conversion of Agilent .d files to mzML as a service, leaving it there.


- Work with LBL DevOps to provide and document sufficient tooling for it to be deployed by non-me; remove gap between local development and deployment

  - Used Kubernetes

- Implement an analytical workflow for genotype analysis



#### Hold

- Establish a paradigm for automated triggering of analysis

- More complicated than we thought and we don’t have the volume for this to be necessary right now. This should be pursued in the context of a broader, more cohesive vision for how devices, generally, interface with the infrastructure that takes signals from them and turns that into structured information.
