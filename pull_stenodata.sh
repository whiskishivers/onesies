#!/bin/bash

# Pull stenographer data from each server to local directories.

SERVERS=(
	"10.1.1.12,steno2"
	"10.1.1.13,steno3"
	"10.1.1.14,steno4"
	"10.1.1.15,steno5"
	"10.1.1.16,steno6"
)

run_rsync() {
	# Args: $1: IP, $2: Local dir
	rsync -rh -e "ssh -q" --stats --exclude=".*" --chmod=F644 ops@$1:/data/stenographer/ $2 &&
	echo "[*] Successful $1 pull."
}

# Start rsync job for each server.
for i in ${SERVERS[@]}
do
	IFS=',' read -r -a array <<< "$i"
	IP="${array[0]}"
	HOSTNAME="${array[1]}"

	echo "[ ] Starting $IP pull."
	run_rsync $IP /data/$HOSTNAME/steno &

	# Limit concurrent jobs
	while [ $(jobs -r | wc -l) -ge 4 ]
	do
		sleep 1
	done

done

wait

echo "Script finished."
