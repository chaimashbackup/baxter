#!/bin/bash

if [ "${1}" = "enable" ]
then
    rosrun baxter_tools enable_robot.py -e
elif [ "${1}" = "disable" ]
then
    rosrun baxter_tools enable_robot.py -d
elif [ "${1}" = "reset" ]
then
    rosrun baxter_tools enable_robot.py -r
else
    echo "Unknown command. Use enable|disable|reset ."
fi
