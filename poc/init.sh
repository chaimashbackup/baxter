#!/bin/bash

sudo ip addr add 10.0.0.250/24 dev enp2s0

ping -c 3 10.0.0.221

../scripts/baxter.sh enable

ip a

./server_mt.py
