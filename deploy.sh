#!/bin/bash

pkill -f "python3 run.py" > /dev/null 2>&1
source ~/miniconda3/bin/activate feishu
nohup python3 run.py > output.log 2>&1 &
