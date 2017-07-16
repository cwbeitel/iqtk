
set -e

ubuntu_version=$(cat /etc/issue | grep -i ubuntu | awk '{print $2}' | \
  awk -F'.' '{print $1}')

apt-get update

#if [[ "$ubuntu_version" == "14" ]]; then
#fi

apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libcurl4-openssl-dev \
    openjdk-8-jdk \
    openjdk-8-jre-headless \
    pkg-config \
    python-dev \
    python-setuptools \
    python-virtualenv \
    python3-dev \
    python3-setuptools \
    rsync \
    sudo \
    unzip \
    wget \
    zip \
    zlib1g-dev

apt-get install -y ca-certificates-java
update-ca-certificates -f

apt-get clean
rm -rf /var/lib/apt/lists/*
