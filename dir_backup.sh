#!/bin/bash

# Use scp to download files one directory at a time to a mounted device.
# When a directory is complete, remove the files.

MOUNTED_DIR=/media/mint/backup
REMOTE_DIR=/data

# Sanity checks
[ ! -d $MOUNTED_DIR ] && echo "$MOUNTED_DIR is not a directory." && exit 1
[ ! $(findmnt $MOUNTED_DIR) ] && echo "$MOUNTED_DIR has no mounted filesystem." && exit 1

# Get remote directory listing
ssh user@10.0.0.1 find $REMOTE_DIR -type d > dirs.txt

for wd in $(cat dirs.txt)
do
	# Create download directory and copy files
	mkdir -pv $MOUNTED_DIR/$wd &&
	scp user@10.0.0.1:$REMOTE_DIR/$wd/* $MOUNTED_DIR/$wd &&

	# All files downloaded, now delete remote files.
	ssh user@10.0.0.1 rm $REMOTE_DIR/$wd/*
done

# TODO: maybe clean up empty dirs on the remote end
# maybe exclude empty dirs from dir list download
