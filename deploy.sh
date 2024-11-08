#!/bin/bash

nohup conda run -n feishu python /srv/feishu/run.py > /srv/feishu/output.log 2>&1 &
