#!/bin/bash

# Download files to an attached hard drive, then delete off disk using the web API.
# Usage example: ./script.sh 1 500

BASE_URL="http://localhost:5000/record"
DOWNLOAD_DIR="/media/mint/elements" # Full path to mounted hard drive
JOB_LIMIT=50

run_curl() {
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"
	cd $DOWNLOAD_DIR
	(curl -f -sSOJL $DATA_URL &&
	curl -sX DELETE $DELETE_URL -o /dev/null &&
	echo -n ".") ||
	sleep 1
}

# Run only if the dir has a mounted device
if [ -z "$(mount | grep "on $DOWNLOAD_DIR type")" ]
then
	echo "No mounted device found for $DOWNLOAD_DIR!"
	exit 1
fi

START=$1
END=$2
JOBCOUNT_PEAK=0
echo "Downloading to $DOWNLOAD_DIR..."
while [ $START -lt $(($END+1)) ]
do
	# Run curl if the job limit isn't reached
	JOB_COUNT=$(jobs -r | wc -l)
	if [ $JOB_COUNT -lt $JOB_LIMIT ]
	then
		run_curl $START &
		START=$(($START+1))
	else
		#wait $!
		sleep 0.3
	fi
	
	# Performance testing stuff
	if [ $JOB_COUNT -gt $JOBCOUNT_PEAK ]
	then
		JOBCOUNT_PEAK=$JOB_COUNT
	fi
done

wait
echo "Done!"
# echo $JOBCOUNT_PEAK
