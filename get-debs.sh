#!/usr/bin/bash

# Download installed packages for an offline repo

mkdir -p debs
cd debs
dpkg -l | grep "^ii" | awk '{print $2}' | xargs -n 20 apt-get download

echo "Creating repository index..."
apt-ftparchive packages . > Packages
apt-ftparchive release . > Release

echo "Finished."

