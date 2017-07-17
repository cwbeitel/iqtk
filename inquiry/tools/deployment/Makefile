GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create inquiry \
		--scopes "cloud-platform" \
		--num-nodes 4
	gcloud container clusters get-credentials inquiry

.PHONY: deploy-fission-core
deploy-fission-core:
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-rbac.yaml
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-cloud.yaml

.PHONY: deploy-fission-logger
deploy-fission-logger:
	kubectl create -f https://raw.githubusercontent.com/fission/fission/master/fission-logger.yaml

.PHONY: deploy-fission-ui
deploy-fission-ui:
	kubectl create -f https://raw.githubusercontent.com/fission/fission-ui/master/docker/fission-ui.yaml

.PHONY: deploy-fission-nats
deploy-fission-nats:
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-nats.yaml

.PHONY: deploy-fission
deploy-fission: deploy-fission-core deploy-fission-ui deploy-fission-logger deploy-fission-nats

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
  gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/inquiry .

.PHONY: push
push: build
	gcloud docker -- push gcr.io/$(GCLOUD_PROJECT)/inquiry

.PHONY: create-service
create-service:
	kubectl create -f iqtk-service.yaml

.PHONY: create-deployment
create-deployment:
	kubectl create -f iqtk-deployment.yaml

.PHONY: deploy
deploy: create-service create-deployment

.PHONY: delete
delete:
	-kubectl delete -f iqtk-frontend.yaml
	-kubectl delete -f iqtk-worker.yaml
	-kubectl delete -f iqtk-frontend.yaml
