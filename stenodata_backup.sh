#!/bin/bash

# Copy paired packet an index stenographer files to a remote
# share. This keeps the paired files together when backup devices are swapped.

# Local stenographer directories
PACKET_DIR=/data/stenographer/packets
INDEX_DIR=/data/stenographer/index

# Remote location that contains packets/ and index/ directories.
REMOTE_DIR=/mnt/backup


mkdir -p $REMOTE_DIR/packets $REMOTE_DIR/index

# Copy each packet file and related index file
for f in $(find $PACKET_DIR -type f)
do
	FNAME=$(basename $f)
	rsync --chmod=F644 $f $REMOTE_DIR/packets &&
	rsync --chmod=F644 $INDEX_DIR/$FNAME $REMOTE_DIR/index
done
