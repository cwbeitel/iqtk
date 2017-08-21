#################################################################
# Dockerfile
#
# Version:          1
# Software:         GATK
# Software Version: 3.4
# Description:      The Genome Analysis Toolkit or GATK is a software package developed at the Broad Institute to analyze high-throughput sequencing data.
# Website:          https://www.broadinstitute.org/gatk/|https://github.com/broadgsa/gatk-protected/
# Tags:             Genomics
# Provides:         gatk 3.4|samtools 1.2|bwakit 0.7.12|picard tools 1.139
# Base Image:       java:7
# Build Cmd:        docker build --rm -t biodckrdev/gatk 3.4/.
# Pull Cmd:         docker pull biodckrdev/gatk
# Run Cmd:          docker run --rm -it biodckrdev/gatk <options> <files>
#################################################################
#SOURCE: https://github.com/giantswarm/giantswarm-gatk/blob/master/Dockerfile
# Source Image
FROM java:7

# Set noninterative mode
ENV DEBIAN_FRONTEND noninteractive

################## BEGIN INSTALLATION ######################
#
# Change to root
#
USER root

#
# INSTALL MAVEN
#
RUN apt-get update -qq && \
    apt-get install -y -q --fix-missing \
      libncurses5-dev  \
      libncursesw5-dev \
      build-essential \
      bzip2 \
      zlib1g-dev \
      maven && \
    apt-get clean && \
    apt-get purge && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir /data /config

#
# Add biodocker user with password biodocker
#
RUN useradd --create-home --shell /bin/bash --user-group --uid 1000 --groups sudo biodocker && \
    echo `echo "biodocker\nbiodocker\n" | passwd biodocker`

#
# Change user
#
USER biodocker

#
# Create $HOME/bin folder
#
RUN mkdir -p /home/biodocker/bin

#
# Add $HOME/bin to path
#
ENV PATH=$PATH:/home/biodocker/bin
ENV HOME=/home/biodocker


ENV DST=/home/biodocker/bin
ENV FOLDER=gatk

RUN git clone https://github.com/broadgsa/gatk-protected.git $DST/$FOLDER && \
    cd $DST/$FOLDER && \
    git reset --hard $SHA && \
    mvn verify && \
    bash -c 'echo -e "#!/bin/bash\njava -jar '$DST/$FOLDER'/target/GenomeAnalysisTK.jar  \$@" > '$DST'/GenomeAnalysisTK' && \
    chmod +x $DST/GenomeAnalysisTK

ENV PATH=/usr/lib/jvm/java-7-openjdk-amd64/bin:$PATH

#ENV JAVABIN=/usr/lib/jvm/java-7-openjdk-amd64/bin/java
#ENTRYPOINT ["java", "-jar", "$DST/target/GenomeAnalysisTK.jar"]

#
# Share default volumes
#
VOLUME ["/data", "/config"]

CMD ["GenomeAnalysisTK"]
