project=jbei-cloud
version=0.0.1
tool=msconvert
tag=gcr.io/${project}/${tool}:${version}

echo building $tag
docker build -t ${tag} .
gcloud docker -- push ${tag}
