#!/bin/bash

# Download files to an attached hard drive, then delete off disk using the web API.
# Usage example: ./script.sh 1 500

BASE_URL="http://localhost:5000/record"
MOUNT_DIR="/media/$USER/elements" # Full path to mounted hard drive
DOWNLOAD_DIR="$(hostname)_$(date +%Y%m%d_%H%M)"
JOB_LIMIT=25

run_curl() {
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"
	(curl -f -sSOJL $DATA_URL &&
	curl -sX DELETE $DELETE_URL -o /dev/null) ||
	sleep 1
}

# Check for mounted device.
[ -z "$(mount | grep "on $MOUNT_DIR type")" ] &&
	echo "No device mounted to $MOUNT_DIR" &&
	exit 1

START=$1
END=$2
JOBCOUNT_PEAK=0

# Create download directory on device
cd $MOUNT_DIR
mkdir -p $DOWNLOAD_DIR
cd $DOWNLOAD_DIR

echo "Downloading to $(pwd)"
while [ $START -lt $(($END+1)) ]
do
	# Run curl if the job limit isn't reached
	JOB_COUNT=$(jobs -r | wc -l)
	if [ $JOB_COUNT -lt $JOB_LIMIT ]
	then
		echo -n "."
		run_curl $START &
		START=$(($START+1))
	else
		#wait
		sleep 0.1
	fi
	
	# Performance testing stuff
	if [ $JOB_COUNT -gt $JOBCOUNT_PEAK ]
	then
		JOBCOUNT_PEAK=$JOB_COUNT
	fi
done

wait
ls -lh
echo "Done!"
#echo "Job peak: $JOBCOUNT_PEAK"
