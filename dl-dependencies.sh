#bin/bash

# Download a package from the repo, including dependencies

if [ -z $1 ]; then 
	echo "Usage: ./dl-dependencies.sh <pkg>"
	exit 1;
fi


TOPDIR=$(realpath $(dirname $0))

mkdir -p $TOPDIR/$1/dependencies &&
cd $TOPDIR/$1 &&
apt-get download $1 &&
cd dependencies
apt-get download $(apt-cache depends $1 | grep "Depends:" | awk '{print $2}' | grep -v "<")

# Install downloaded packages
#apt-get install ./*.deb
