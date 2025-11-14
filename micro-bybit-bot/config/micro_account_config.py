import os
import logging
from decimal import Decimal

class MicroConfig:
    # Bybit Configuration
    BYBIT_TESTNET = os.getenv('BYBIT_TESTNET', 'true').lower() == 'true'
    API_KEY = os.getenv('BYBIT_API_KEY', '')
    API_SECRET = os.getenv('BYBIT_API_SECRET', '')
    
    # Account Configuration
    INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', '100.00'))
    MAX_PORTFOLIO_EXPOSURE = 0.60  # 60% of account
    MAX_CONCURRENT_TRADES = 8
    DAILY_LOSS_LIMIT = 0.10  # 10% daily loss limit
    
    # Position Sizing
    BASE_RISK_PER_TRADE = 0.01  # 1% per trade
    MIN_POSITION_SIZE = 5.00  # $5 minimum
    MAX_POSITION_SIZE = 15.00  # $15 maximum
    
    # Leverage
    DEFAULT_LEVERAGE = 3
    
    # Scanner Settings
    SCAN_INTERVAL = 300  # 5 minutes
    MAX_SYMBOLS_TO_SCAN = 50
    MIN_24H_VOLUME = 1000000  # $1M volume
    
    # Scalping Settings
    SCALP_TAKE_PROFIT = 0.015  # 1.5%
    SCALP_STOP_LOSS = 0.010    # 1.0%
    SCALP_TIMEFRAME = '3m'
    MAX_HOLD_TIME = 300  # 5 minutes
    
    # Risk Management
    MAX_DRAWDOWN = 0.20  # 20% max drawdown
    CIRCUIT_BREAKER = 0.15  # Stop at 15% loss
    
    # Performance
    TRACK_PERFORMANCE = True
    PERFORMANCE_REPORT_INTERVAL = 1800  # 30 minutes

class MicroLogger:
    @staticmethod
    def setup():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/micro_trading.log'),
                logging.StreamHandler()
            ]
        )

CONFIG = MicroConfig()