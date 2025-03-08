#!/bin/bash

# ✅ Stop any existing bot process
echo "🔴 Stopping existing bot process..."
pkill -f bot.py

# ✅ Move to the project directory
cd /home/ubuntu/trading_bot || {
    echo "❌ Failed to change directory"
    exit 1
}

# ✅ Load environment variables from .env
if [ -f ".env" ]; then
    export $(cat .env | xargs)
else
    echo "❌ .env file not found"
    exit 1
fi

# ✅ Activate virtual environment
if [ -d "tradebot_env" ]; then
    source tradebot_env/bin/activate
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# ✅ Start the bot using nohup (keeps it running after logout)
echo "🚀 Starting the trading bot..."
nohup python3 bot.py > logs/trading_bot.log 2>&1 &

# ✅ Store the process ID (PID) for easier stopping later
echo $! > trading_bot.pid

# ✅ Check if the bot is running
sleep 2
if ps -p $(cat trading_bot.pid) > /dev/null; then
    echo "✅ Trading bot is running (PID: $(cat trading_bot.pid))"
else
    echo "❌ Failed to start trading bot"
fi
