# deploy-services

Deployment of the workflow manager service on Kubernetes.

A recommended pre-requisite for these steps is the developer quickstart, [here](https://github.com/iqtk/iqtk/blob/master/inquiry/docs/developer/developer-quickstart.md).

## Build and deploy flow service

The flow service container can be built with the following command:

```
export IQTK_DEPLOY_VERSION=deploy-devel
sh scripts/build_container.sh
docker push quay.io/iqtk/iqtk:$IQTK_DEPLOY_VERSION
```

Then deployed to run on the kubernetes cluster via

```
sh scripts/deploy_kube_services.sh
```

Logs from these services can then be viewed with the following which we are inspecting to verify they are free of credential errors (meaning the google account credential secret was deployed correctly):

```bash
kubectl logs -l app=iqtk
```
