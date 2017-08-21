# deploy-services

Deployment of flow trigger and runner services on kubernetes.

## Configuration testing

Before attempting the real deployment we can first test our cluster is configured correctly in terms of both the honcho startup processes and the shared service account credentials secret. We'll do this by deploying a simplified mock of planned `iqtk` container and inspect logs as to whether (1) each of the intended processes was started within each deployment, and (2) whether each of those received the necessary credentials to publish messages to a dummy PubSub topic.

This dev container can be built and pushed to quay with the following:

```bash
export IQTK_DEPLOY_VERSION=deploy-devel
sh scripts/build_dev_container.sh
docker push quay.io/iqtk/iqtk:depoy-devel
```

Once the push has completed we can deploy the development services with the following:

```bash
sh scripts/deploy_kube_services.sh
```

Logs from these services can then be viewed with the following which we are inspecting to verify they are free of credential errors (meaning the google account credential secret was deployed correctly):

```bash
kubectl logs -l app=iqtk
```

TODO: Minikube should be sufficient for this kind of testing obviating need for image push and pull.

## Deploying the production container

After verifying the cluster configuration in the above we can go ahead and deploy the production `iqtk` container built using the `inquiry/tools/ci_build/...` infrastructure and released under the `quay.io/iqtk/iqtk:[numeric version]` tag pattern.

E.g. if the container version is 0.0.1:

```bash
export IQTK_DEPLOY_VERSION=0.0.1
sh scripts/deploy_kube_services.sh
```

The health of this deployment can then be verified by examining the following for errors, as above:

```bash
kubectl logs -l app=iqtk
```

TODO: Full run through to verify correctness of all commands from clean env.
