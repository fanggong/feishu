#!/bin/bash

pkill -f run.py || true
nohup conda run -n feishu python3 /srv/feishu/run.py > /srv/feishu/output.log 2>&1 &
