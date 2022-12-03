#!/bin/bash

# If a filesystem is nearing a storage limit percentage, do things

MOUNTPOINT=/data
STORAGE_LIMIT=99

pgrep storage-check | grep -v $$ && exit

# Check for mounted filesystem
findmnt $MOUNTPOINT > /dev/null || exit 1

# Report usage, and exit if not over the limit
USED=$(findmnt $MOUNTPOINT -f -n -o USE% | awk '{ print $1 }' | sed 's/%//' || exit 1)
if [ $USED -lt $STORAGE_LIMIT ]
then
	echo "$(date +%D\ %r) - $MOUNTPOINT is at $USED%. Exiting."
	exit 0
else
	echo "$(date +%D\ %r) - $MOUNTPOINT is at $USED%. Storage limit ($STORAGE_LIMIT%) exceeded!"
fi


### Storage is over the limit, code to do things goes here ###
echo "oh lawd its over the limit"
