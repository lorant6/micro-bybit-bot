import asyncio
import aiohttp
import logging
from pybit.unified_trading import HTTP
from config.micro_account_config import CONFIG

class MicroBybitClient:
    """Simplified Bybit client for $100 account"""
    
    def __init__(self):
        self.session = HTTP(
            testnet=CONFIG.BYBIT_TESTNET,
            api_key=CONFIG.API_KEY,
            api_secret=CONFIG.API_SECRET
        )
        self.logger = logging.getLogger(__name__)
    
    async def get_available_symbols(self) -> list:
        """Get available symbols"""
        try:
            response = self.session.get_instruments_info(category="linear")
            return [item['symbol'] for item in response['result']['list']]
        except Exception as e:
            self.logger.error(f"Error getting symbols: {e}")
            return []
    
    async def get_ticker(self, symbol: str) -> dict:
        """Get ticker info"""
        try:
            response = self.session.get_tickers(category="linear", symbol=symbol)
            if response['result']['list']:
                return response['result']['list'][0]
            return {}
        except Exception as e:
            self.logger.debug(f"Error getting ticker for {symbol}: {e}")
            return {}
    
    async def get_klines(self, symbol: str, interval: str, limit: int) -> list:
        """Get kline data"""
        try:
            response = self.session.get_kline(
                category="linear",
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            return response['result']['list']
        except Exception as e:
            self.logger.debug(f"Error getting klines for {symbol}: {e}")
            return []
    
    async def set_leverage(self, symbol: str, leverage: int):
        """Set leverage"""
        try:
            self.session.set_leverage(
                category="linear",
                symbol=symbol,
                buyLeverage=str(leverage),
                sellLeverage=str(leverage)
            )
        except Exception as e:
            self.logger.debug(f"Error setting leverage: {e}")
    
    async def place_order(self, symbol: str, side: str, order_type: str, 
                         qty: float, stop_loss: float = None, 
                         take_profit: float = None) -> dict:
        """Place order"""
        try:
            order_params = {
                "category": "linear",
                "symbol": symbol,
                "side": side,
                "orderType": order_type,
                "qty": str(qty),
                "timeInForce": "GTC"
            }
            
            if stop_loss:
                order_params["stopLoss"] = str(stop_loss)
            if take_profit:
                order_params["takeProfit"] = str(take_profit)
                
            response = self.session.place_order(**order_params)
            return response['result']
        except Exception as e:
            self.logger.error(f"Error placing order: {e}")
            return {}
    
    async def get_account_balance(self) -> float:
        """Get account balance"""
        try:
            response = self.session.get_wallet_balance(accountType="UNIFIED")
            if response['result']['list']:
                return float(response['result']['list'][0]['totalWalletBalance'])
            return CONFIG.INITIAL_CAPITAL
        except Exception as e:
            self.logger.error(f"Error getting balance: {e}")
            return CONFIG.INITIAL_CAPITAL