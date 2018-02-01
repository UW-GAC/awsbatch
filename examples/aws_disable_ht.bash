#!/bin/sh
# disable hyperthreading for all instance types except t* (e.g., t2.large)

# get instance type
it="$(curl --silent http://169.254.169.254/latest/meta-data/instance-type)"

# check if starts with it
if [[ $it == t* ]]; then
    echo "No hyperthreading for $it"
    exit 1
fi

echo "Disabling hyperthreading for $it"
for cpunum in $(cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list | cut -s -d, -f2- | tr ',' '\n' | sort -un)
do
	echo 0 > /sys/devices/system/cpu/cpu$cpunum/online
done
