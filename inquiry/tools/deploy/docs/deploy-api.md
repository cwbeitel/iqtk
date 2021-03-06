# deploy-api

Here we'll walk through deployment of the Inquiry API endpoint and API service on Kubernetes which will have the following steps:
* Obtain the necessary credentials
* Deploy the Google Cloud Endpoints API endpoint
* Deploy the API service on Kubernetes

Before attempting this make sure you have already deployed and configured your kubernetes cluster as described in the

### Obtaining an OAuth client ID and API key

The first step is to obtain the necessary credentials and keys. We'll need the following:
* An API key
* An OAuth client ID and credentials file.
* A service account key

The first step is to obtain the OAuth client ID, and API key information, see [documentation](https://developers.google.com/youtube/analytics/registering_an_application).

We recommend storing keys and key paths in a file that can be sourced to restore these variables into the shell environment - the fields of [export_secrets.tmpl.sh](https://github.com/iqtk/iqtk/blob/master/inquiry/tools/deploy/export_secrets.sh) can can be modified in this way.


Storing this and other secret variables in a non-versioned shell script that can be sourced to restore these is a recommended step.

##### *Important point*:
It is very important to ensure that your service account credentials remain secure - both on the machines on which they are stores as well as preventing them from being committed to version control.

### Endpoint deployment

An endpoint can be deployed (having defined the OAUTH_CLIENT_ID as above) on Google Endpoints using the following command:

```bash
sh scripts/deploy_api_endpoint.sh
...
Service Configuration [2017-08...] uploaded for service [....appspot.com]
...
```

This will generate an endpoint service config name and ID in the form above but no need to write them down, these will be obtained by the following script.

### API service deployment

The API service can be deployed either on App Engine or Kubernetes. The latter is somewhat more complex.

#### API deployment on GAE

The API service can be deployed on App Engine with the following command (requiring confirmation):

```bash
sh scripts/deploy_api_gae.sh
```

Note that this step requires having deployed the API endpoint in the previous step so if you have issues here try repeating the previous step.

#### API deployment on Kubernetes

The API can be deployed on kubernetes with the following command:

```bash
sh scripts/deploy_api_kube.sh
```

TODO: This doesn't currently work.

### Testing API deployment

Once deployed you can then test the API is functioning with the following command:

```bash
iqtk-client-devel health
```
