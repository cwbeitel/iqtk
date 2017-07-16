FROM ubuntu:14.04

COPY install/*.sh /install/

RUN /install/bootstrap_deb_packages.sh
RUN add-apt-repository -y ppa:openjdk-r/ppa
RUN /install/install_deb_packages.sh
RUN /install/install_bazel.sh
RUN /install/install_pip_packages.sh

RUN echo 'export PATH=$PATH:/root/bin' >> ~/.bashrc

COPY install/.bazelrc ~/bazel/bazel.bazelrc
