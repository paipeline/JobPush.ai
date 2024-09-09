#!/bin/bash
source .venv/bin/activate
python src/main.py


echo "Starting Node.js application..."
yarn install
yarn start &
NODE_PID=$!

echo "Starting Python job search script..."
python src/main.py

wait $!

echo "Stopping Node.js application..."
kill $NODE_PID

# 退出Python虚拟环境(如果使用了虚拟环境)
deactivate

echo "Job search completed and Node.js application stopped."