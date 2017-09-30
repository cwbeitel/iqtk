# deploy-api

Here we'll walk through deployment of the Inquiry API endpoint and API service on Kubernetes which will have the following steps:
* Obtain the necessary credentials
* Deploy the Google Cloud Endpoints API endpoint
* Deploy the API service on Kubernetes

Pre-requisites for these steps is the [developer quick start](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/developer/developer-quickstart.md) and [cluster deployment](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/developer/deploy-cluster.md).

### Obtaining an OAuth client ID and API key

The first step is to obtain the necessary credentials and keys. We'll need the following:
* An API key
* An OAuth client ID and credentials file.
* A service account key

The first step is to obtain the OAuth client ID, and API key information, see [documentation](https://developers.google.com/youtube/analytics/registering_an_application).

We recommend storing keys and key paths in a file that can be sourced to restore these variables into the shell environment - the fields of [export_secrets.tmpl.sh](https://github.com/iqtk/iqtk/blob/master/inquiry/tools/deploy/export_secrets.sh) can can be modified in this way.

Steps to create a service account key file are provided [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys).

##### *Important point*:
It is very important to ensure that your service account credentials remain secure - both on the machines on which they are stores as well as preventing them from being committed to version control.

### Endpoint deployment

An endpoint can be deployed (having defined the OAUTH_CLIENT_ID variable) on Google Endpoints using the following command:

```bash
sh scripts/deploy_api_endpoint.sh
...
Service Configuration [2017-08...] uploaded for service [....appspot.com]
...
```

This will generate an endpoint service config name and ID in the form above but no need to write them down, these will be obtained by the following script.

### API deployment on Kubernetes

The API can be deployed on kubernetes with the following command:

```bash
sh scripts/deploy_api_kube.sh
```

Once deployed you can then test the API is functioning with the following command:

```bash
API_SERVICE_IP=[???]
API_PORT=[???]
curl -H "content-type:application/json" http://${API_SERVICE_IP}:${API_PORT}/health
```

### Run API tests

In developing the API we'll want to be able to run tests. We can run those outside of the deployment container as follows:

```bash
bazel test //inquiry/services:api_test --test_output=errors
```

TODO: Explain developer workflow, probably elsewhere, whereby
