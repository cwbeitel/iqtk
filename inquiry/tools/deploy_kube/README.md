# Deployment on Kubernetes

**DRAFT**

## Creating a service account

Please start by referring to the gcloud documentation [on creating a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts). Once that is created, we'll create a role from the gcloud console "IAM & Admin > Roles > Create Role". Name it `iqtk-actor` and grant the permissions listed under "Editor".

TODO: Currently using "Editor" permissions because unclear which permissions are required by ggenomics operations. But by creating a role and assigning that to the SA we can change these on the fly without having to re-deploy our key secret.

TODO: Make the creation of this SA and assignment of the role programmatic.

Lastly, under "IAM & Admin > IAM > Add" enter the email address of the service account you created and in the "Roles" dropdown under "Custom" select "iqtk-actor".

## Local testing

We can test run the service within the `iqtk` Docker container in the following way. This step should be useful for verifying that your service account key is configured correctly.

```bash
LOCAL_SA_KEY_JSON=[/some/path/key.json]
docker run -v ${LOCAL_SA_KEY_JSON}:/key \
  -e "GOOGLE_APPLICATION_CREDENTIALS=/key/key.json" \
  -e "CLOUDSDK_CORE_PROJECT=ml-beam" \
  -it quay.io/iqtk/iqtk:0.0.3 python -m inquiry.framework.service
```

## Deployment

If all is well you're ready to deploy this key as a Kubernetes secret:

```bash
kubectl create secret generic gcloud-app-credentials-secret \
  --from-file=key.json=${LOCAL_SA_KEY_JSON}
```

Before we create the `iqtk-service` deployment you'll need to edit the value field of `CLOUDSDK_CORE_PROJECT` in `config/iqtk.yaml` to the name of your Google Cloud Platform project. (TODO: This should be programmatic.)

Then create the cluster and deploy `iqtk-service`.

```bash
sh deploy_kube.sh
```

You can check in on the status of the deployment by pulling logs

```bash
(iqtk5) ➜ kubectl logs -l app=iqtk
No handlers could be found for logger "oauth2client.contrib.multistore_file"
2017-08-01 14:34:59 iqtk-service-623362695-8kn78 google_auth_httplib2[1] DEBUG Making request: POST https://accounts.google.com/o/oauth2/token
No handlers could be found for logger "oauth2client.contrib.multistore_file"
2017-08-01 14:35:16 iqtk-service-623362695-mzbnd google_auth_httplib2[1] DEBUG Making request: POST https://accounts.google.com/o/oauth2/token
No handlers could be found for logger "oauth2client.contrib.multistore_file"
2017-08-01 14:35:00 iqtk-service-623362695-qhgz2 google_auth_httplib2[1] DEBUG Making request: POST https://accounts.google.com/o/oauth2/token
```

or listing the status of deployed services

```bash
(iqtk5) ➜ kubectl get deployments
NAME           DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
iqtk-service   3         3         3            3           7m
```

In the latter, the available column will switch from 0 to the number of replicas specified in config/iqtk.yaml when the service is deployed. Likewise

For additional reference, see the gcloud docs on [authenticating a Kubernetes deployment with gcloud](https://cloud.google.com/container-engine/docs/tutorials/authenticating-to-cloud-pubsub).

## Debug

Deployment of both the initial cluster and the `iqtk` service does take a few minutes. In the mean time you may see logs like the following:

```bash
(iqtk) ➜ kubectl logs -l app=iqtk
Error from server (BadRequest): container "iqtk-service" in pod "iqtk-service-623362695-8kn78" is waiting to start: ContainerCreating
```

Also important is the fact that your deployment will stall in this state until the 'google-app-credentials-secret' secret has been created as described above. It's recommended you do this before deploying the service but if you forgot you should still be able to do it and the pods will eventually pick up the credentials and become available.
