import pandas as pd
import numpy as np
from typing import List

class EfficientIndicators:
    """Efficient technical indicators"""
    
    @staticmethod
    def ema(prices: List[float], period: int) -> float:
        """Exponential Moving Average"""
        series = pd.Series(prices)
        return series.ewm(span=period, adjust=False).mean().iloc[-1]
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> float:
        """Relative Strength Index"""
        series = pd.Series(prices)
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else 50
    
    @staticmethod
    def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
        """Average True Range"""
        df = pd.DataFrame({'high': highs, 'low': lows, 'close': closes})
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = abs(df['high'] - df['close'].shift())
        df['tr3'] = abs(df['low'] - df['close'].shift())
        df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        atr = df['tr'].rolling(period).mean()
        return atr.iloc[-1] if not atr.empty else 0
    
    @staticmethod
    def bollinger_bands(prices: List[float], period: int = 20, std_dev: int = 2) -> dict:
        """Bollinger Bands"""
        series = pd.Series(prices)
        sma = series.rolling(window=period).mean()
        std = series.rolling(window=period).std()
        
        return {
            'upper': sma.iloc[-1] + (std.iloc[-1] * std_dev),
            'middle': sma.iloc[-1],
            'lower': sma.iloc[-1] - (std.iloc[-1] * std_dev)
        }