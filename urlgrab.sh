#!/bin/bash

# Download files to an attached hard drive, then delete off disk using the web API.
# Usage example: ./script.sh 1 500

BASE_URL="http://localhost:5000/record"
MOUNT_DIR="/media/$USER/elements"
DOWNLOAD_DIR="$HOSTNAME_$(date +%Y%m%d_%H%M)"
JOB_LIMIT=4

START=$1
END=$2
JOBCOUNT_PEAK=0

run_curl() {
	DATA_URL="$BASE_URL/$1/data"
	DELETE_URL="$BASE_URL/$1"
	(/usr/bin/curl -f -sSOJL $DATA_URL &&
	/usr/bin/curl -sX DELETE $DELETE_URL -o /dev/null && return 0) ||
	sleep 1 && return 1
}

# Check for mounted device.
[ -z "$(mount | grep "on $MOUNT_DIR type")" ] &&
	echo "No device mounted to $MOUNT_DIR" &&
	exit 1

# Create download directory on device
cd $MOUNT_DIR
mkdir -pv $DOWNLOAD_DIR

cd $DOWNLOAD_DIR
echo "Downloading to $PWD"
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

	[ $JOB_COUNT -gt $JOBCOUNT_PEAK ] && JOBCOUNT_PEAK=$JOB_COUNT
done

wait

echo "Done!"
#ls -lh
echo "Job peak: $JOBCOUNT_PEAK"
