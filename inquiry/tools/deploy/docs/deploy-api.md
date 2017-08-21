# deploy-api

Deployment of the Inquiry API endpoint and API service on Google App Engine.

### Obtaining an oauth client ID

TODO: Link to info on how to obtain a client ID

The client ID should then be set to the following variable.

```bash
export IQTK_OAUTH_CLIENT_ID=[your oauth client ID]
```

Storing this and other secret variables in a non-versioned shell script that can be sourced to restore these is a recommended step.

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
