#!/bin/bash

# Base port for sitl <-> GCS connection
BASEPORT=4444
# Command to run SITL

# 63.98504,-22.654108000000008,30.0,89.0
command1="./arducopter -S --model copter --speedup 1 --base-port ${BASEPORT} --slave 0 --defaults copter.parm -I0"

# Command to run GCS mavproxy
command2="mavproxy.py --master=tcp:127.0.0.1:${BASEPORT} --out=udp::14553"

# Open the SITL tab
gnome-terminal --tab --title="SITL" -- bash -c "$command1"

# Open the GCS tab
gnome-terminal --tab --title="GCS" -- bash -c "$command2"


