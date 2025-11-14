import asyncio
import logging
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from utils.micro_bybit import MicroBybitClient
from modules.nano_risk import NanoRiskManager
from config.micro_account_config import CONFIG

@dataclass
class MicroPosition:
    symbol: str
    direction: str
    entry_price: float
    quantity: float
    stop_loss: float
    take_profit: float
    order_id: str
    entry_time: float
    pnl: float = 0

class MicroScalpingEngine:
    """Micro scalping engine for $100 account"""
    
    def __init__(self, risk_manager: NanoRiskManager):
        self.risk_manager = risk_manager
        self.client = MicroBybitClient()
        self.logger = logging.getLogger(__name__)
        self.active_positions: Dict[str, MicroPosition] = {}
        self.performance = {
            'total_trades': 0, 'winning_trades': 0,
            'total_pnl': 0, 'daily_pnl': 0
        }
    
    async def execute_micro_scalps(self, opportunities: List[Dict]):
        """Execute micro scalp trades"""
        if not self.risk_manager.can_trade():
            self.logger.warning("Trading paused by risk manager")
            return
        
        current_positions = len(self.active_positions)
        max_new_trades = CONFIG.MAX_CONCURRENT_TRADES - current_positions
        
        if max_new_trades <= 0:
            return
        
        executed = 0
        for opportunity in opportunities[:max_new_trades]:
            symbol = opportunity['symbol']
            
            if not self.risk_manager.can_trade_symbol(symbol):
                continue
            
            success = await self._execute_micro_scalp(opportunity)
            if success:
                executed += 1
                await asyncio.sleep(0.5)
        
        if executed > 0:
            self.logger.info(f"Executed {executed} micro scalp trades")
    
    async def _execute_micro_scalp(self, opportunity: Dict) -> bool:
        """Execute single micro scalp"""
        try:
            symbol = opportunity['symbol']
            direction = opportunity['direction']
            current_price = opportunity['current_price']
            
            position_size = self._calculate_micro_position_size(symbol, current_price)
            if position_size < CONFIG.MIN_POSITION_SIZE:
                return False
            
            stop_loss, take_profit = self._calculate_scalp_levels(
                direction, current_price, CONFIG.SCALP_STOP_LOSS, CONFIG.SCALP_TAKE_PROFIT
            )
            
            if not self.risk_manager.approve_trade(symbol, position_size, stop_loss, take_profit):
                return False
            
            await self.client.set_leverage(symbol, CONFIG.DEFAULT_LEVERAGE)
            
            order = await self.client.place_order(
                symbol=symbol,
                side='Buy' if direction == 'LONG' else 'Sell',
                order_type='Market',
                qty=position_size,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if order and order.get('order_id'):
                position = MicroPosition(
                    symbol=symbol, direction=direction,
                    entry_price=current_price, quantity=position_size,
                    stop_loss=stop_loss, take_profit=take_profit,
                    order_id=order['order_id'], entry_time=time.time()
                )
                
                self.active_positions[order['order_id']] = position
                self.logger.info(f"💰 MICRO SCALP: {direction} {symbol} Size: ${position_size:.2f}")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error executing micro scalp: {e}")
            return False
    
    def _calculate_micro_position_size(self, symbol: str, current_price: float) -> float:
        """Calculate position size"""
        from config.top_500_micro import PRICE_TIERS
        
        base_risk = CONFIG.INITIAL_CAPITAL * CONFIG.BASE_RISK_PER_TRADE
        
        if symbol in PRICE_TIERS['under_1']:
            position_size = min(base_risk * 1.5, CONFIG.MAX_POSITION_SIZE)
        elif symbol in PRICE_TIERS['over_100']:
            position_size = min(base_risk * 0.7, CONFIG.MAX_POSITION_SIZE)
        else:
            position_size = min(base_risk, CONFIG.MAX_POSITION_SIZE)
        
        position_size = max(CONFIG.MIN_POSITION_SIZE, position_size)
        position_size = min(CONFIG.MAX_POSITION_SIZE, position_size)
        
        return position_size
    
    def _calculate_scalp_levels(self, direction: str, entry_price: float, 
                               stop_loss_pct: float, take_profit_pct: float) -> tuple:
        """Calculate SL/TP levels"""
        if direction == 'LONG':
            stop_loss = entry_price * (1 - stop_loss_pct)
            take_profit = entry_price * (1 + take_profit_pct)
        else:
            stop_loss = entry_price * (1 + stop_loss_pct)
            take_profit = entry_price * (1 - take_profit_pct)
        
        return stop_loss, take_profit
    
    async def monitor_micro_positions(self):
        """Monitor positions"""
        current_time = time.time()
        positions_to_close = []
        
        for order_id, position in list(self.active_positions.items()):
            try:
                hold_time = current_time - position.entry_time
                if hold_time > CONFIG.MAX_HOLD_TIME:
                    positions_to_close.append((order_id, position, "Time expiry"))
                    continue
                
                exit_signal = await self._check_manual_exit(position)
                if exit_signal:
                    positions_to_close.append((order_id, position, exit_signal))
                
                await self._update_position_pnl(position)
                
            except Exception as e:
                self.logger.error(f"Error monitoring position: {e}")
        
        for order_id, position, reason in positions_to_close:
            await self._close_micro_position(order_id, position, reason)
    
    async def _check_manual_exit(self, position: MicroPosition) -> Optional[str]:
        """Check manual exit conditions"""
        try:
            ticker = await self.client.get_ticker(position.symbol)
            if not ticker:
                return None
            
            current_price = float(ticker.get('lastPrice', 0))
            
            if position.direction == 'LONG':
                pnl_pct = (current_price - position.entry_price) / position.entry_price
            else:
                pnl_pct = (position.entry_price - current_price) / position.entry_price
            
            if pnl_pct < -0.02:
                return "Emergency exit"
            
            if pnl_pct > 0.008:
                return "Early profit"
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Error checking manual exit: {e}")
            return None
    
    async def _update_position_pnl(self, position: MicroPosition):
        """Update position PnL"""
        try:
            ticker = await self.client.get_ticker(position.symbol)
            if not ticker:
                return
            
            current_price = float(ticker.get('lastPrice', 0))
            
            if position.direction == 'LONG':
                position.pnl = (current_price - position.entry_price) * position.quantity
            else:
                position.pnl = (position.entry_price - current_price) * position.quantity
                
        except Exception as e:
            self.logger.debug(f"Error updating PnL: {e}")
    
    async def _close_micro_position(self, order_id: str, position: MicroPosition, reason: str):
        """Close position"""
        try:
            close_side = 'Sell' if position.direction == 'Buy' else 'Buy'
            
            order = await self.client.place_order(
                symbol=position.symbol,
                side=close_side,
                order_type='Market',
                qty=position.quantity,
                reduce_only=True
            )
            
            if order:
                self._update_performance(position)
                del self.active_positions[order_id]
                self.logger.info(f"✅ MICRO CLOSE: {position.symbol} PnL: ${position.pnl:.2f}")
                
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
    
    def _update_performance(self, position: MicroPosition):
        """Update performance"""
        self.performance['total_trades'] += 1
        self.performance['total_pnl'] += position.pnl
        self.performance['daily_pnl'] += position.pnl
        
        if position.pnl > 0:
            self.performance['winning_trades'] += 1
    
    def get_performance(self) -> Dict:
        """Get performance"""
        win_rate = (self.performance['winning_trades'] / self.performance['total_trades'] * 100) if self.performance['total_trades'] > 0 else 0
        
        return {
            'total_trades': self.performance['total_trades'],
            'winning_trades': self.performance['winning_trades'],
            'win_rate': win_rate,
            'total_pnl': self.performance['total_pnl'],
            'daily_pnl': self.performance['daily_pnl'],
            'active_positions': len(self.active_positions)
        }
    
    def get_active_positions_count(self) -> int:
        return len(self.active_positions)