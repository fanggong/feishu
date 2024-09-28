#!/bin/bash

conda activate feishu
conda env update --file environment.yml --prune
cp /root/config.py /srv/feishu/config.py
pkill -f main.py
nohup python3 main.py > output.log 2>&1 &