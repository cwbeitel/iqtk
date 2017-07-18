# deployment `iqtk` cluster

Here is where we will keep configs and scripts related to deploying an `iqtk` cluster on GKE. See the Makefile for details on the steps and their dependencies. Those steps are primarily as follows:

Deploy a kubernetes cluster:

```bash
make create-cluster
```

Deploy the necessary pods and services:

```bash
make deploy
```

TODO: Substantial work in progress. Currently Fission is not used and planning short-term bootstrap using separate processes to (1) receive from PubSub and relay to NATS and (2) receive from NATS and run `iqtk` to initiate workflows.
