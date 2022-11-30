#!/bin/bash

# Print IP address if it is in an arp response
# -I <interface name> might be needed for arping command

do_arp() {
	arping -f -q -c1 -w1 10.1.3.$1 && echo "10.1.3.$1"
}

for i in $(seq 1 254)
do
	do_arp $i &
	sleep 0.1

done

wait
