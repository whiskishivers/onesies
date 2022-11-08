#!/bin/bash

# Download files and then delete them using the web API.
# Usage example: ./script.sh 1 500

JOB_LIMIT=30 # Maximum concurrent requests/downloads
BASE_URL='http://localhost:5000/record'
START=$1
END=$2

run_curl() {
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"

	curl -f -C- -sSOJL $DATA_URL &&
	curl -sX DELETE $DELETE_URL -o /dev/null

	if [ $? -eq 0 ]
	then
		RESULT="." # Success
	else
		RESULT="!" # Error
	fi
	echo -n $RESULT
}

cd "$(dirname $0)" # TODO: Check for mounted drive, cd to mounted directory
echo "Downloading to $(pwd)"

while [ $START -lt $(($END+1)) ]
do
	# Run function while process count is below threshold
	JOB_COUNT=$(pgrep -c -u $USER curl)
	if [ $JOB_COUNT -lt $JOB_LIMIT ]
	then
		run_curl $START &
		START=$(($START+1))
	else
		sleep 0.1
	fi
done

wait
echo -e "\nDone!"

