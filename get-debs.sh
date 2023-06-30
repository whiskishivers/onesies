#!/usr/bin/bash

# Download installed packages for an offline repo

touch uris.txt
touch installed.txt
mkdir -p debs

# Make a list of repo uris to download
apt list --installed | cut -d"/" -f1 | tail -n +2 > installed.txt
xargs apt-get install --reinstall --print-uris < installed.txt | grep ^\'"htt" | cut -d"'" -f2 > uris.txt

# Download packages and make required repo files
cd debs && wget -i ../uris.txt -nc -nv && cd ..
apt-ftparchive packages . > Packages
apt-ftparchive release . > Release

