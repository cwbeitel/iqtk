# deploy-cluster

A kubernetes cluster can be deployed and corresponding credentials obtained with the following (provided you've run `gcloud auth login` and set a working project with `gcloud config set project [project_id]`):

```bash
sh scripts/deploy_kube.sh
```

Note that re-issuing this command will not re-create the cluster if it already exists for the active Google Cloud account (doing so will only re-obtain the `kubectl` credentials for that cluster).

Once the cluster is deployed we can list pods, deployments, and services running on the cluster with the `kubectl get pods`, `kubectl get deployments`, and `kubectl get services` commands.

Notably, all logs related to the iqtk deployments can be viewed with the following:

```bash
kubectl logs -l app=iqtk
```

## Creating a service account

In order to deploy services that require Google service account authentication please start by referring to the gcloud documentation [on creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts). Once that is created, we'll create a role from the gcloud console "IAM & Admin > Roles > Create Role". Name it `iqtk-actor` and grant the permissions listed under "Editor".

TODO: Currently using "Editor" permissions because unclear which permissions are required by ggenomics operations. But by creating a role and assigning that to the SA we can change these on the fly without having to re-deploy our key secret.

TODO: Make the creation of this SA and assignment of the role programmatic.

Lastly, under "IAM & Admin > IAM > Add" enter the email address of the service account you created and in the "Roles" dropdown under "Custom" select "iqtk-actor".

## Deployment of credentials secret

If all is well you're ready to deploy this key as a Kubernetes secret:

```bash
kubectl create secret generic gcloud-app-credentials-secret \
  --from-file=key.json=${LOCAL_SA_KEY_JSON}
```

For additional reference, see the gcloud docs on [authenticating a Kubernetes deployment with gcloud](https://cloud.google.com/container-engine/docs/tutorials/authenticating-to-cloud-pubsub).

#### Next steps

Once the following steps are completed, you're ready to deploy the workflow trigger and runner services, check out [that documentation here](deploy-services.md).
