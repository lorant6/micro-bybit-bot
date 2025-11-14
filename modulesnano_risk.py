import logging
from typing import Dict
from config.micro_account_config import CONFIG

class NanoRiskManager:
    """Risk manager for $100 account"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.daily_pnl = 0
        self.total_trades_today = 0
        self.symbol_exposure: Dict[str, float] = {}
        self.is_trading_enabled = True
    
    async def initialize(self):
        """Initialize risk manager"""
        self.logger.info("🛡️ Initializing Nano Risk Manager")
        self.daily_pnl = 0
        self.total_trades_today = 0
        self.symbol_exposure = {}
    
    def can_trade(self) -> bool:
        """Check if trading allowed"""
        if not self.is_trading_enabled:
            return False
        
        if self.daily_pnl <= -CONFIG.DAILY_LOSS_LIMIT * CONFIG.INITIAL_CAPITAL:
            self.logger.warning(f"Daily loss limit reached: ${self.daily_pnl:.2f}")
            self.is_trading_enabled = False
            return False
        
        total_pnl = self.daily_pnl
        if total_pnl <= -CONFIG.MAX_DRAWDOWN * CONFIG.INITIAL_CAPITAL:
            self.logger.warning(f"Max drawdown reached: ${total_pnl:.2f}")
            self.is_trading_enabled = False
            return False
        
        return True
    
    def can_trade_symbol(self, symbol: str) -> bool:
        """Check if symbol can be traded"""
        current_exposure = self.symbol_exposure.get(symbol, 0)
        if current_exposure >= 1:
            return False
        return True
    
    def approve_trade(self, symbol: str, position_size: float, 
                     stop_loss: float, take_profit: float) -> bool:
        """Approve trade"""
        if not self.can_trade():
            return False
        
        if not self.can_trade_symbol(symbol):
            return False
        
        if position_size < CONFIG.MIN_POSITION_SIZE:
            return False
        
        if position_size > CONFIG.MAX_POSITION_SIZE:
            return False
        
        risk = abs(stop_loss - take_profit)
        if risk > position_size * 0.5:
            return False
        
        return True
    
    def record_trade(self, symbol: str, position_size: float, pnl: float = 0):
        """Record trade"""
        self.total_trades_today += 1
        self.daily_pnl += pnl
        self.symbol_exposure[symbol] = self.symbol_exposure.get(symbol, 0) + 1
    
    def record_trade_close(self, symbol: str, pnl: float):
        """Record trade close"""
        self.daily_pnl += pnl
        if symbol in self.symbol_exposure:
            self.symbol_exposure[symbol] = max(0, self.symbol_exposure[symbol] - 1)
    
    def get_risk_metrics(self) -> Dict:
        """Get risk metrics"""
        return {
            'daily_pnl': self.daily_pnl,
            'total_trades_today': self.total_trades_today,
            'trading_enabled': self.is_trading_enabled,
            'symbol_exposure': self.symbol_exposure
        }
    
    def reset_daily_metrics(self):
        """Reset daily metrics"""
        self.daily_pnl = 0
        self.total_trades_today = 0
        self.symbol_exposure = {}
        self.is_trading_enabled = True