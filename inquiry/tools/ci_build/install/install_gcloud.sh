export CLOUDSDK_CORE_DISABLE_PROMPTS=1
curl https://sdk.cloud.google.com | bash
echo PATH='${HOME}/google-cloud-sdk/bin/:${PATH}' >> ${HOME}/.bashrc
bash ${HOME}/.bashrc
gcloud components update preview
