#!/bin/sh

# Make internal Docker IP address available to processes.
export INTERNAL_IP=`ip route get 1 | awk '{print $NF;exit}'`
# Replace Startup Variables
if test SILENT = '1'; then
	MODIFIED_STARTUP=`eval $(echo ${STARTUP} | sed -e 's/{{/${/g' -e 's/}}/}/g')`
	echo $MODIFIED_STARTUP
else
	MODIFIED_STARTUP=$(echo ${STARTUP} | sed -e 's/{{/${/g' -e 's/}}/}/g')
fi
# Run the Server
eval ${MODIFIED_STARTUP}
