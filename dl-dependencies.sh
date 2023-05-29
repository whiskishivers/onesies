#!/bin/bash

# Download packages found in pkgs.txt and all dependencies (recursive).

get_deb() {
        echo " * Downloading $1..."
        apt-get download -qq $1 2>/dev/null &&
        cd dependencies &&
        for i in $(apt-rdepends -s DEPENDS $1 | grep "^\w" | sort -u);
        do
                apt-get download -qq $i 2>/dev/null
        done
}

apt-get update || exit 1

echo "Downloading packages found in pkgs.txt..."

mkdir -p dependencies

for i in $(cat pkgs.txt); do
        get_deb $i &
        while [ $(jobs -r | wc -l) -gt 9 ]; do
                sleep 0.1
        done
done
wait
echo "Script finished."
