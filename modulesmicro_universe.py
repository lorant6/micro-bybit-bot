import asyncio
import logging
from typing import Dict, List, Set
from utils.micro_bybit import MicroBybitClient
from config.micro_account_config import CONFIG
from config.top_500_micro import TOP_50_MICRO, SYMBOL_CATEGORIES, PRICE_TIERS

class MicroUniverseManager:
    """Manages trading universe for $100 account"""
    
    def __init__(self):
        self.client = MicroBybitClient()
        self.logger = logging.getLogger(__name__)
        self.active_symbols: Set[str] = set()
        self.symbol_metrics: Dict[str, Dict] = {}
        self.available_balance = CONFIG.INITIAL_CAPITAL
        
    async def initialize(self):
        """Initialize universe"""
        self.logger.info("💰 Initializing Micro Universe...")
        self.active_symbols = set(TOP_50_MICRO)
        await self._verify_symbols()
        await self._load_initial_metrics()
        self.logger.info(f"✅ Micro Universe Ready: {len(self.active_symbols)} symbols")
    
    async def _verify_symbols(self):
        """Verify symbol availability"""
        try:
            available_symbols = set()
            all_bybit_symbols = await self.client.get_available_symbols()
            
            for symbol in TOP_50_MICRO:
                if symbol in all_bybit_symbols:
                    available_symbols.add(symbol)
            
            self.active_symbols = available_symbols
        except Exception as e:
            self.logger.error(f"Error verifying symbols: {e}")
            self.active_symbols = set(TOP_50_MICRO)
    
    async def _load_initial_metrics(self):
        """Load initial metrics"""
        for symbol in list(self.active_symbols)[:20]:
            try:
                ticker = await self.client.get_ticker(symbol)
                if ticker:
                    self.symbol_metrics[symbol] = {
                        'last_price': float(ticker.get('lastPrice', 0)),
                        'volume_24h': float(ticker.get('volume24h', 0))
                    }
                await asyncio.sleep(0.1)
            except Exception as e:
                self.logger.debug(f"Error loading metrics for {symbol}: {e}")
    
    def get_tradable_symbols(self) -> List[str]:
        return list(self.active_symbols)
    
    def get_symbols_by_volume(self, min_volume: float = 0) -> List[str]:
        symbols = []
        for symbol in self.active_symbols:
            metrics = self.symbol_metrics.get(symbol, {})
            if metrics.get('volume_24h', 0) >= min_volume:
                symbols.append(symbol)
        return symbols
    
    def get_symbol_metrics(self, symbol: str) -> Dict:
        return self.symbol_metrics.get(symbol, {})
    
    def update_balance(self, new_balance: float):
        self.available_balance = new_balance
    
    def get_balance(self) -> float:
        return self.available_balance