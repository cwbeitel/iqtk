#! /bin/bash
echo ${SA_KEY} | base64 --decode > gcloud.p12
gcloud auth activate-service-account ${SA_EMAIL} --key-file gcloud.p12
ssh-keygen -f ~/.ssh/google_compute_engine -N ""
