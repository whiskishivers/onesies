#!/bin/bash

# Download packages found in pkgs.txt and all dependencies (recursive) for an offline repo.

get_deb() {
	echo " * Downloading $1..."
	cd debs
	apt-get download -qq $1 2>/dev/null &&

	for i in $(apt-rdepends -s DEPENDS $1 | grep "^\w" | sort -u); do
		apt-get download -qq $i 2>/dev/null
	done
}

apt-get update || exit 1
mkdir -p offline-repo
cd offline-repo
mkdir -p debs

echo "Downloading packages found in pkgs.txt..."
for i in $(cat pkgs.txt); do
	get_deb $i &
	while [ $(jobs -r | wc -l) -gt 19 ]; do
		sleep 0.1
	done
done
wait

# Create required repo files.
apt-ftparchive packages . > Packages
apt-ftparchive release . > Release

echo "Script finished."
