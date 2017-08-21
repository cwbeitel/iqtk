FROM r-base:3.3.1

RUN apt-get update -qq \
        && apt-get dist-upgrade -y

RUN apt-get update -qq \
        && apt-get install  -y  \
                curl \
                netcdf-bin \
                libnetcdf-dev \
                libxml2-dev \
                libssl-dev

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile

RUN Rscript -e "source('http://bioconductor.org/biocLite.R'); biocLite('devtools'); biocLite('Biobase'); biocLite('BiocGenerics'); biocLite('ProtGenerics'); biocLite('zlibbioc')"

RUN Rscript -e "source('http://bioconductor.org/biocLite.R'); library(devtools); install_github('sneumann/mzR', branch='boost_159', repos=biocinstallRepos())"

RUN rm -rf /var/lib/apt/lists/* && apt-get update

RUN Rscript -e "source('http://bioconductor.org/biocLite.R'); biocLite('lgatto/MSnbase');"

RUN Rscript -e "source('http://bioconductor.org/biocLite.R'); library(devtools); install_github('sneumann/xcms', ref='xcms3', repos=biocinstallRepos())"

WORKDIR /mnt/data

