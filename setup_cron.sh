#!/bin/bash

# 获取Python解释器的路径
PYTHON_PATH=$(which python3)

# 获取job_fetch.py脚本的路径
SCRIPT_PATH="./src/job_fetch.py"

# 添加cron任务
(crontab -l 2>/dev/null; echo "0 9 * * * $PYTHON_PATH $SCRIPT_PATH") | crontab -
(crontab -l 2>/dev/null; echo "0 13 * * * $PYTHON_PATH $SCRIPT_PATH") | crontab -
(crontab -l 2>/dev/null; echo "0 20 * * * $PYTHON_PATH $SCRIPT_PATH") | crontab -

echo "Cron jobs have been set up to run job_fetch.py at 9 AM, 1 PM, and 8 PM every day."