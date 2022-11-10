#!/bin/bash
SCRIPT_DIR=$PWD
# ROS_BAXTER =/./home/lev/rethink_ws
export ROS_IP=10.0.0.250
export ROS_MASTER_URI=http://10.0.0.221:11311

cd
cd rethink_ws
. ./devel/setup.bash 

cd $SCRIPT_DIR


