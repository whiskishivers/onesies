#!/bin/bash

# Connect to remote servers, copy stenographer data and index files to local directories.

SERVERS=( "10.1.3.102,steno2" "10.1.3.103,steno3" "10.1.3.104,steno4" "10.1.3.105,steno5" "10.1.3.106,steno6" )

for i in ${SERVERS[@]}
do
	IFS=',' read -r -a array <<< "$i"
	IP="${array[0]}"
	HOSTNAME="${array[1]}"
	echo "Started pull from $IP."
	rsync -r --exclude=".*" --chmod=F644 ops@$IP:/data/stenographer/packets/ /data/$HOSTNAME/steno/packets &
	rsync -r --exclude=".*" --chmod=F644 ops@$IP:/data/stenographer/index/ /data/$HOSTNAME/steno/index &

	# Limit to four concurrent jobs
	while [ $(jobs -r | wc -l) -ge 4 ]
	do
		sleep 0.1
	done
done

wait

echo "Script finished."


