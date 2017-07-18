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
	# TODO: Some of these won't work with --validate=false and I'm guessing that means there's
	# a non-insignificant issue to fix.
	# TODO: Check whether these are already deployed instead of attempting and failing.
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-rbac.yaml --validate=false
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-cloud.yaml --validate=false

.PHONY: deploy-fission-logger
deploy-fission-logger:
	kubectl create -f https://raw.githubusercontent.com/fission/fission/master/fission-logger.yaml --validate=false

.PHONY: deploy-fission-ui
deploy-fission-ui:
	kubectl create -f https://raw.githubusercontent.com/fission/fission-ui/master/docker/fission-ui.yaml --validate=false

.PHONY: deploy-fission-nats
deploy-fission-nats:
	kubectl create -f https://github.com/fission/fission/releases/download/nightly20170705/fission-nats.yaml --validate=false

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
	kubectl create -f iqtk-service.yaml --validate=false

.PHONY: create-deployment
create-deployment:
	kubectl create -f iqtk-deployment.yaml --validate=false

.PHONY: deploy
deploy: deploy-fission create-service create-deployment

.PHONY: delete
delete:
	-kubectl delete -f iqtk-frontend.yaml
	-kubectl delete -f iqtk-worker.yaml
	-kubectl delete -f iqtk-frontend.yaml
