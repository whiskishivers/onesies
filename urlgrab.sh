#!/bin/bash

# Download files and then delete them using the web API.
# Usage example: ./script.sh 1 500

JOB_LIMIT=30 # Maximum concurrent requests/downloads
BASE_URL='http://localhost:5000/record'
STARTING_DIR=$(pwd)
START=$1
END=$2

run_curl() {
	# Download data, then send delete request.
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"

	(curl -f -C- -sSOJL $DATA_URL &&
	 curl -sX DELETE $DELETE_URL -o /dev/null &&
	 echo -n ".")
}

# TODO: Need correct path for mounted drive before this works...
#if [ -n "$(mount | grep " on /media/$USER/label")" ]
#then
#	cd /media/$USER/label
#else
#	echo "Hard drive is not mounted, or mounted to the wrong dir."
#	exit 1
#fi

cd $(dirname $0)
echo "Starting downloads to $(pwd)..."

while [ $START -lt $(($END+1)) ]
do
	# Run function while process count is below threshold
	JOB_COUNT=$(jobs -r | wc -l)
	if [ $JOB_COUNT -lt $JOB_LIMIT ]
	then
		run_curl $START &
		START=$(($START+1))
	else
		# wait $!
		sleep 0.1
	fi
done

wait
cd $STARTING_DIR
echo -e "\nDone!"

