#!/bin/bash
set -x

echo "🔴 Stopping existing bot process..."
pkill -f bot.py

# ✅ Change to the project directory
cd /home/ubuntu/trading_bot || {
    echo "❌ Failed to change directory"
    exit 1
}

# ✅ Load environment variables from .env
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
else
    echo "❌ .env file not found"
    exit 1
fi

# ✅ Activate virtual environment
source /home/ubuntu/trading_bot/tradebot_env/bin/activate

# ✅ Create logs directory if it doesn't exist
mkdir -p logs

# ✅ Start the bot using nohup
echo "🚀 Starting the trading bot..."
nohup /home/ubuntu/trading_bot/tradebot_env/bin/python bot.py > logs/trading_bot.log 2>&1 &
echo $! > /home/ubuntu/trading_bot/trading_bot.pid

# ✅ Check if the bot is running
sleep 2
if ps -p $(cat /home/ubuntu/trading_bot/trading_bot.pid) > /dev/null; then
    echo "✅ Trading bot is running (PID: $(cat /home/ubuntu/trading_bot/trading_bot.pid))"
else
    echo "❌ Failed to start trading bot"
fi
