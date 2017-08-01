FROM ubuntu:14.04

COPY install/*.sh /install/

RUN /install/bootstrap_deb_packages.sh
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN /install/install_deb_packages.sh
RUN /install/install_bazel.sh
RUN /install/install_pip_packages.sh

RUN echo 'export PATH=$PATH:/root/bin' >> ~/.bashrc

COPY install/.bazelrc ~/bazel/bazel.bazelrc

RUN curl https://sdk.cloud.google.com | bash
ENV PATH="${HOME}/google-cloud-sdk/bin/:${PATH}"
RUN echo PATH='${HOME}/google-cloud-sdk/bin/:${PATH}' >> ${HOME}/.bashrc
RUN ${HOME}/google-cloud-sdk/bin/gcloud components update
