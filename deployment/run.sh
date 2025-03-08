#!/bin/bash

# Stop any existing bot process
echo "🔴 Stopping existing bot process..."
pkill -f bot.py

# Move to the project directory
cd /home/ubuntu/trading_bot/deployment || {
    echo "❌ Failed to change directory"
    exit 1
}

# Load environment variables from .env
if [ -f "../.env" ]; then
    set -a
    source ../.env
    set +a
else
    echo "❌ .env file not found"
    exit 1
fi

# Activate virtual environment
if [ -d "../tradebot_env" ]; then
    source ../tradebot_env/bin/activate
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Start the bot using nohup
echo "🚀 Starting the trading bot..."
nohup python3 ../bot.py > ../logs/trading_bot.log 2>&1 &
echo $! > ../trading_bot.pid

# Check if the bot is running
sleep 2
if ps -p $(cat ../trading_bot.pid) > /dev/null; then
    echo "✅ Trading bot is running (PID: $(cat ../trading_bot.pid))"
else
    echo "❌ Failed to start trading bot"
fi
