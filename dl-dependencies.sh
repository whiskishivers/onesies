#bin/bash

# Download a deb package with required dependencies to disk. Not recursive!

if [ -z $1 ]; then 
	echo "Usage: ./dl-dependencies.sh <pkg>"
	exit 1;
fi

apt-get download $1 && \
apt-get download $(apt-cache depends $1 | grep "Depends:" | awk '{print $2}')

# Install downloaded packages
#apt-get install ./*.deb
