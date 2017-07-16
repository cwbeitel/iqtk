set -e

# Install bootstrap dependencies from ubuntu deb repository.
apt-get update
apt-get install -y --no-install-recommends \
    software-properties-common
apt-get clean
rm -rf /var/lib/apt/lists/*
