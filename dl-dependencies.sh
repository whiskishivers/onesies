#!/usr/bin/bash

# Download packages that are installed to debs/

touch uris.txt
mkdir -p debs

for i in $(apt list --installed | cut -d"/" -f1); do
	apt-get install --reinstall --print-uris $i | grep "^'http" | cut -d "'" -f2 | tee -a uris.txt &
	
	while [ $(jobs -r | wc -l) -gt 9 ]; do
		sleep 0.1
	done
done
wait

cd debs && wget -i ../uris.txt -nc -nv && cd ..
apt-ftparchive packages . > Packages
apt-ftparchive release . > Release
