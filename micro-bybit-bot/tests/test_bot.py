"""
Basic tests for Micro Trading Bot
"""

import pytest
import asyncio
from utils.efficient_indicators import EfficientIndicators

def test_indicators():
    """Test technical indicators"""
    indicators = EfficientIndicators()
    
    # Test EMA
    prices = [100, 101, 102, 103, 104, 105]
    ema = indicators.ema(prices, 3)
    assert ema > 0
    
    # Test RSI
    rsi = indicators.rsi(prices, 3)
    assert 0 <= rsi <= 100
    
    print("✅ Basic indicator tests passed")

def test_config():
    """Test configuration"""
    from config.micro_account_config import CONFIG
    
    assert CONFIG.INITIAL_CAPITAL == 100
    assert CONFIG.MAX_CONCURRENT_TRADES == 8
    assert CONFIG.DAILY_LOSS_LIMIT == 0.10
    
    print("✅ Configuration tests passed")

if __name__ == "__main__":
    test_indicators()
    test_config()
    print("🎉 All tests passed!")