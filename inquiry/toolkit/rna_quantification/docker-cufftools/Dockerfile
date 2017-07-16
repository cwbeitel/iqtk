# Set the base image to Ubuntu
FROM biocontainers/biocontainers

RUN conda install -y cufflinks==2.2.1

RUN apt-get clean all && \
    apt-get update && \
    apt-get install -y  wget

RUN mkdir /tmp/th && \
  wget https://ccb.jhu.edu/software/tophat/downloads/tophat-2.1.1.Linux_x86_64.tar.gz \
  -O /tmp/th/tophat.tar.gz

# DEFINE DEFAULT COMMAND
CMD ["cufflinks"]
