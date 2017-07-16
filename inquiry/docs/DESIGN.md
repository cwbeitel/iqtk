
# Inquiry Research Infrastructure
#### Design Document

## Purpose

The purpose of this project is to make available to the broader scientific research community a comprehensive biological data science research infrastructure with primary project goals that include the following (todo discuss more):

1. Reproducibility

2. Robust automation

3. Abstraction and increased leverage

4. Structured data warehousing and partial unification of community data space

For a comprehensive exposition of the problem and requirements we refer the reader to the DARPA Synergistic Discovery and Design [call for proposals](https://www.fbo.gov/utils/view?id=6d8044bb740578b628515f8bf70f5733).

## Architecture

The following provides an overview of the system architecture followed by numbered per-component narratives.

![CircleCI](inquiry/docs/assets/arch.png)

1. Laboratory Instrument
  - E.g. MiSeq, Agilent SomeModel Mass Spectrometer with attached windows machine controller.
  - Data is automatically mirrored to (2) using BeyondCompare (?).

2. Institute-local storage server and uplink
  - Running (on the samba server / attached to it) is a tool that periodically runs gsutil rsync and logs to cloud logging

3. Cloud storage for raw instrument data
  - All instrument-generated data is synced to a Google Cloud Storage bucket designated for data backup and long-term storage with separate sub-sections for the instrument of origin.

4. Storage object change notification
  - When new data arrives in the raw cloud data storage space a storage object change notification is fired issuing this message over PubSub.
  - See [the Object Change Notification](https://cloud.google.com/storage/docs/object-change-notification) documentation for more details.
  - The schema for storage changed messages is as follows: (TODO)

5. Job submission entry-point (automated trigger and admin)
  - Storage changed PubSub messages are received by the storage changed listener and used to parameterize calls to the iqtk workflow initiator.
  - Alternatively workflows can be initiated in an ad-hoc manner by administrator users.

6. Workflow orchestration
  - Regardless of means, workflow initiation triggers a run on the workflow orchestration system (currently built to use Cloud DataFlow).
  - Workflows may be composed of a heterogeneous set of batch task initiators and traditional Apache Beam transforms.

7. Batch task message
  - Some workflow steps initiate a batch task message sent to the `batch-submit` PubSub topic.
  - The schema for these messages is as follows: (TODO)

8. Batch task manager
  - A Kubernetes cluster running on Google Container Engine
  - Workers receive batch task messages (7) via PubSub and translate these into Kubernetes Job objects.
  - Job objects are submitted to a secondary Kubernetes cluster (9) running on Google Container Engine.

9. Batch task pool
  - A Kubernetes cluster running on Google Container Engine. Pods are launched and job scripts are executed following stage-in of specified requisite data followed by stage-out of resultant data.

10. BigQuery structured data warehouse
  - Key resultant data structures are written to BigQuery tables according to community-standard data schemas.
  - We currently focus primarily on data schemas provided by the Global Alliance for Genomics and Health (GA4GH), see [here](https://github.com/ga4gh/ga4gh-schemas/tree/master/src/main/proto/ga4gh) for more details.

11. Jupyter notebook via. cloud console
  - Presently most efficient way seems to be to allow people to run a datalab instance from cloud shell avoiding significant setup that is a hindrance to lab users.
  - This also is a way for people to access their experimental data without building a UI.

12. Instrument event message stream
  - We are currently discussing the best way to pull logs and sensor data off of our instruments (including robotic work-cells, alive/dead, run state of various instruments...) in a generalized way.
