#!/bin/bash

# If a filesystem is nearing a storage limit percentage, do things

MOUNTPOINT=/data
STORAGE_LIMIT=90


# Report usage, and exit if not over the limit

USED=$(df $MOUNTPOINT --output=pcent | tail -n 1 | awk '{ print $1 }' | sed 's/%//' || exit 1)

if [ $USED -lt $STORAGE_LIMIT ]
then
	echo "$(date +%D\ %r) - $MOUNTPOINT usage: $USED%. Exiting."
	exit 0
else
	echo "$(date +%D\ %r) - $MOUNTPOINT usage: $USED%. Storage limit ($STORAGE_LIMIT%) exceeded."
fi


### Storage is over the limit, code to do things goes here ###

df -h $MOUNTPOINT
