#!/usr/bin/bash

# Download installed packages for an offline repo

touch uris.txt
touch installed.txt
mkdir -p debs

# Make a list of repo uris to download
apt list --installed | cut -d"/" -f1 | tail -n +2 > installed.txt
xargs apt-get install --reinstall --print-uris < installed.txt | grep ^\'http | cut -d"'" -f2 > uris.txt

# Download packages and make required repo files
cd debs
echo "Downloading new files..."
xargs -a ../uris.txt wget -N -nv
cd ..
echo "Creating repository index..."
apt-ftparchive packages . > Packages
apt-ftparchive release . > Release

echo "Finished."

