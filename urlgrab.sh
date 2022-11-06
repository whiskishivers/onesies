#!/bin/bash

# Download files and then delete them using the web API.
# Usage example: ./script.sh 1 500

JOBCOUNT=20 # Maximum concurrent requests/downloads
ENDPOINT='http://localhost:5000/image/'
START=$1
END=$2

run_curl() {
	curl -f -C- -sSOJL $ENDPOINT$1 &&
	curl -sX DELETE $ENDPOINT$1 -o /dev/null
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
	if [ $(pgrep curl 2>/dev/null | wc -l) -lt $JOBCOUNT ]
	then
		run_curl $START &
		START=$(($START+1))
	else
		sleep 0.1
	fi
done

wait
echo -e "\nDone!"

