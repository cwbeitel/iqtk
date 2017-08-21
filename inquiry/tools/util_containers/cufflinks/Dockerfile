FROM ubuntu:latest
# File Author / Maintainer
MAINTAINER Douglas McCloskey <dmccloskey87@gmail.com>
# Install wget
RUN apt-get update && apt-get install -y wget \
      autotools-dev   \
        curl            \
        grep            \
        sed             \
        git             \
        wget            \
        zip             \
        build-essential \
        pkg-config      \
        python          \
        python-dev      \
        python-pip      \
        bzip2

# Install cufflinks from http
WORKDIR /usr/local/

RUN wget http://cole-trapnell-lab.github.io/cufflinks/assets/downloads/cufflinks-2.2.1.Linux_x86_64.tar.gz

RUN tar -zxvf cufflinks-2.2.1.Linux_x86_64.tar.gz

# add cufflinks to path
ENV PATH /usr/local/cufflinks-2.2.1.Linux_x86_64:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games

# Cleanup
RUN rm -rf cufflinks-2.2.1.Linux_x86_64.tar.gz
RUN apt-get clean
