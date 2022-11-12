#!/bin/bash

# Download files and then delete them using the web API.
# Usage example: ./script.sh 1 500

#TODO: Check for mounted drive, exit if not found

BASE_URL="http://localhost:5000/record"
DOWNLOAD_DIR=$(pwd)
JOB_LIMIT=30

run_curl() {
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"
	cd $DOWNLOAD_DIR
	curl -f -sSOJL $DATA_URL &&
	curl -sX DELETE $DELETE_URL -o /dev/null &&
	echo -n "."
}

# Run a job for each number in the range.
# Wait if the job count meets the limit.
START=$1
END=$2
echo "Downloading to $DOWNLOAD_DIR..."
while [ $START -lt $(($END+1)) ]
do
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
echo "Done!"

