# Micro Bybit Trading Bot 🚀

A professional trading bot optimized for Bybit with $100 accounts. Features advanced scanning, scalping modules, and institutional-grade risk management for micro accounts.

## 🎯 Features

- **$100 Account Optimized** - Specialized for small accounts
- **Top 50 Cryptocurrencies** - Focus on high-liquidity symbols
- **Advanced Scanning** - Real-time opportunity detection
- **Micro Scalping** - Quick, small-profit trades
- **Nano Risk Management** - Prevents account blow-up
- **Real-time Monitoring** - Live performance tracking

## ⚡ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/lorant6/micro-bybit-bot.git
cd micro-bybit-bot


Steps:

    Clone the repository (if not already done)

    Navigate to the project directory

    Set up the environment (install dependencies, set environment variables)

    Run the bot

Let's break down each step.

Step 1: Clone the repository (if you haven't already)
text

git clone https://github.com/YOUR_USERNAME/micro-bybit-bot.git
cd micro-bybit-bot

Step 2: Set up the environment
text

We have a setup.py script that will:
    - Check Python version
    - Create necessary directories
    - Install dependencies from requirements.txt
    - Create .env file from .env.example

Run:
    python setup.py

Then, edit the .env file with your Bybit testnet API keys.

Step 3: Run the bot
text

We have two main entry points:
    - run_bot.py (recommended)
    - main.py

The run_bot.py script includes additional checks and is the recommended way to start.

Run:
    python run_bot.py

However, note that the bot is designed to run on Bybit testnet first. Make sure you have:
text

- Bybit testnet account: https://testnet.bybit.com/
- Generated API keys from testnet

Let's write the step-by-step instructions in a more detailed way.

Here's a complete step-by-step guide on how to run the trading bot:
🚀 Quick Start Guide
Step 1: Prerequisites

Required Software:

    Python 3.8 or higher

    Git

    Bybit Testnet Account

Check Python Version:
bash

python --version
# or
python3 --version

If you don't have Python, download from python.org
Step 2: Clone and Setup
bash

# Clone your repository
git clone https://github.com/YOUR_USERNAME/micro-bybit-bot.git
cd micro-bybit-bot

# Run the setup script
python setup.py

The setup script will:

    ✅ Check Python version

    ✅ Create necessary directories

    ✅ Install dependencies

    ✅ Create .env file from template

Step 3: Get Bybit API Keys

    Go to Bybit Testnet

    Create an account or log in

    Go to Account → API Management

    Click "Create New Key"

    Set permissions:

        Trade ✅

        Wallet ✅

        Copy Trading ❌

    Get your:

        API Key

        API Secret

Step 4: Configure Environment

Edit the .env file:
bash

# Open the file in a text editor
nano .env
# or use any text editor like Notepad++, VS Code, etc.

Update with your API keys:
bash

# Bybit API Configuration
BYBIT_API_KEY=your_actual_testnet_api_key_here
BYBIT_API_SECRET=your_actual_testnet_api_secret_here
BYBIT_TESTNET=true

# Account Settings
INITIAL_CAPITAL=100

# Trading Settings
MAX_CONCURRENT_TRADES=8
DAILY_LOSS_LIMIT=0.10

Step 5: Run the Bot

Option 1: Simple Runner (Recommended)
bash

python run_bot.py

Option 2: Direct Execution
bash

python main.py

Step 6: Monitor the Bot

When running, you'll see output like:
text

💰 Micro Bybit Trading Bot - $100 Account
==================================================
🛡️ Initializing Nano Risk Manager for $100 account
💰 Initializing Micro Universe...
✅ Micro Universe Ready: 50 symbols
🔍 Performing quick scan...
✅ Quick scan complete: 12 opportunities found
✅ Micro trading system initialized
🎯 Trading with: $100.0
📊 Monitoring: 50 symbols
Entering micro trading loop...

📊 Understanding the Output
Real-time Monitoring

The bot shows:

    Account balance and growth percentage

    Active positions count

    Win rate and total PnL

    Scan results with opportunities found

    Trade executions with entry/exit details

Performance Snapshots (Every 5 minutes)
text

💰 PERFORMANCE SNAPSHOT
Account Balance: $102.50
Account Growth: +2.50%
Total Trades: 8
Win Rate: 62.5%
Total PnL: $2.50
Active Positions: 2

🔧 Configuration Options
Modify Trading Parameters

Edit config/micro_account_config.py:
python

# Position Sizing (default: $5-$15)
MIN_POSITION_SIZE = 5.00
MAX_POSITION_SIZE = 15.00

# Risk Management (default: 10% daily loss)
DAILY_LOSS_LIMIT = 0.10

# Scalping Targets (default: 1.5% TP, 1.0% SL)
SCALP_TAKE_PROFIT = 0.015
SCALP_STOP_LOSS = 0.010

# Trading Speed (default: 5-minute scans)
SCAN_INTERVAL = 300

Add/Remove Trading Symbols

Edit config/top_500_micro.py:
python

# Add your preferred symbols
TOP_50_MICRO = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 
    'SOLUSDT', 'XRPUSDT', 'ADAUSDT',
    # Add more symbols here...
]

🐛 Troubleshooting Common Issues
Issue 1: API Connection Errors

Symptoms:

    "Error getting symbols"

    "Error placing order"

Solutions:
bash

# 1. Verify API keys are correct
# 2. Check internet connection
# 3. Ensure Bybit testnet is accessible
# 4. Verify API permissions (Trade & Wallet)

Issue 2: No Trades Executing

Symptoms:

    Scans find opportunities but no trades

    "Position size too small" messages

Solutions:
bash

# 1. Increase MIN_POSITION_SIZE to $10
# 2. Check symbol liquidity requirements
# 3. Verify risk management settings

Issue 3: Module Import Errors

Symptoms:

    "ModuleNotFoundError"

    Import errors

Solutions:
bash

# Reinstall dependencies
pip install -r requirements.txt

# Or install manually
pip install pybit pandas numpy aiohttp python-dotenv

Issue 4: Python Version Problems

Solutions:
bash

# Check Python version
python --version

# If below 3.8, install newer Python
# On Windows: python.org/downloads
# On Mac: brew install python
# On Linux: sudo apt install python3.8

📈 Monitoring Performance
View Logs
bash

# Real-time log monitoring
tail -f logs/micro_trading.log

# Or open the log file
nano logs/micro_trading.log

Performance Metrics to Watch

    Account Growth: Should be positive over time

    Win Rate: Aim for 55%+

    Average Position Size: $5-$15

    Daily PnL: Monitor for consistency

Risk Management Alerts

The bot will automatically:

    ❌ Stop trading if daily loss exceeds $10

    ❌ Stop trading if total drawdown exceeds $20

    ⚠️ Warn if position sizes are too small/large

🔄 Bot Operation Cycle
Every 5 Minutes:

    Scan - Analyzes 50 cryptocurrencies

    Score - Ranks opportunities by quality

    Execute - Opens positions on top opportunities

    Monitor - Checks existing positions

Continuous:

    Risk Monitoring - Checks account safety

    Position Management - Monitors open trades

    Performance Tracking - Updates metrics

💡 Pro Tips
For Beginners:

    Start with $100 on TESTNET only

    Monitor for first 24 hours before making changes

    Don't modify parameters until you understand them

    Keep logs for troubleshooting

For Advanced Users:

    Adjust position sizing based on risk tolerance

    Modify scanning intervals for faster/slower trading

    Add custom strategies in the strategies folder

    Implement additional risk controls

🛑 Emergency Stop
Manual Stop:
bash

# Press Ctrl+C in the terminal
# The bot will close all positions gracefully

Automatic Stops:

    Daily Loss Limit: $10

    Max Drawdown: $20

    Circuit Breaker: 15% loss

📱 Running in Background
Using nohup (Linux/Mac):
bash

nohup python run_bot.py > bot_output.log 2>&1 &

Using screen (Linux/Mac):
bash

screen -S trading-bot
python run_bot.py
# Press Ctrl+A then D to detach
# screen -r trading-bot to reattach

Using Windows:
bash

# Run in command prompt or PowerShell
python run_bot.py

🔍 Testing Before Live
Step 1: Verify Setup
bash

python tests/test_bot.py

Step 2: Dry Run (No Trades)

Modify modules/micro_scalper.py:
python

# Comment out the order placement
# order = await self.client.place_order(...)
print(f"DRY RUN: Would place {direction} order for {symbol}")

Step 3: Monitor Testnet Performance

    Run for 1-2 weeks on testnet

    Track consistency of results

    Verify risk management works

⚠️ Important Warnings
CRITICAL:

    NEVER use real money until thoroughly tested on testnet

    START WITH $100 ONLY if transitioning to live

    MONITOR DAILY especially in first month

    UNDERSTAND THE RISKS - crypto trading is volatile

Recommended Testing Period:

    Testnet: 2-4 weeks

    Small Live: 1 month with $100

    Scale Up: Only after consistent profitability

🆘 Getting Help
Check Logs First:
bash

cat logs/micro_trading.log | grep "ERROR"

Common Solutions:

    API Issues: Regenerate API keys

    Connection Problems: Check internet/firewall

    No Trades: Adjust position size minimums

    Import Errors: Re-run setup.py

Support:

    Check GitHub Issues for similar problems

    Review the troubleshooting section in README

    Ensure all prerequisites are met

The bot is now ready to run! Remember to always start with testnet and monitor performance closely during the first few days.
