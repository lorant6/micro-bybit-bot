import asyncio
import logging
import signal
import sys
from datetime import datetime
from config.micro_account_config import CONFIG, MicroLogger
from modules.micro_universe import MicroUniverseManager
from modules.efficient_scanner import EfficientScanner
from modules.micro_scalper import MicroScalpingEngine
from modules.nano_risk import NanoRiskManager

class MicroTradingBot:
    """Micro Trading Bot for $100 accounts"""
    
    def __init__(self):
        MicroLogger.setup()
        self.logger = logging.getLogger(__name__)
        
        # Initialize modules
        self.universe = MicroUniverseManager()
        self.risk_manager = NanoRiskManager()
        self.scanner = EfficientScanner(self.universe)
        self.scalper = MicroScalpingEngine(self.risk_manager)
        
        # Bot state
        self.is_running = False
        self.start_time = None
        self.iteration = 0
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    async def start(self):
        """Start the bot"""
        self.logger.info("💰 Starting MICRO Trading Bot - $100 Account")
        self.is_running = True
        self.start_time = datetime.now()
        
        try:
            await self._initialize_system()
            await self._micro_trading_loop()
        except Exception as e:
            self.logger.critical(f"Critical error: {e}")
            await self.stop()
    
    async def _initialize_system(self):
        """Initialize system"""
        self.logger.info("Initializing micro trading system...")
        
        await self.universe.initialize()
        await self.risk_manager.initialize()
        await self.scanner.quick_scan()
        
        self.logger.info("✅ Micro trading system initialized")
        self.logger.info(f"🎯 Trading with: ${CONFIG.INITIAL_CAPITAL}")
        self.logger.info(f"📊 Monitoring: {len(self.universe.active_symbols)} symbols")
    
    async def _micro_trading_loop(self):
        """Main trading loop"""
        self.logger.info("Entering micro trading loop...")
        
        while self.is_running:
            try:
                self.iteration += 1
                
                # Monitor positions
                await self.scalper.monitor_micro_positions()
                
                # Update balance
                current_balance = await self._update_balance()
                self.universe.update_balance(current_balance)
                
                # Check risk
                if not self.risk_manager.can_trade():
                    self.logger.warning("Trading paused - risk limits")
                    await asyncio.sleep(30)
                    continue
                
                # Scheduled operations
                await self._execute_scheduled_operations()
                
                # Performance snapshot
                if self.iteration % 60 == 0:
                    await self._performance_snapshot()
                
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error in iteration {self.iteration}: {e}")
                await asyncio.sleep(10)
    
    async def _execute_scheduled_operations(self):
        """Execute scheduled operations"""
        if self.iteration % 60 == 0:
            await self._scheduled_scan_and_trade()
        
        if self.iteration % 2880 == 0:
            self.risk_manager.reset_daily_metrics()
            self.logger.info("🔄 Daily risk metrics reset")
    
    async def _scheduled_scan_and_trade(self):
        """Scheduled scanning and trading"""
        self.logger.info("🔍 Executing scheduled quick scan...")
        
        try:
            opportunities = await self.scanner.quick_scan()
            top_opps = self.scanner.get_top_opportunities(limit=3)
            
            if top_opps:
                await self.scalper.execute_micro_scalps(top_opps)
            
            total_opps = sum(len(opps) for opps in opportunities.values())
            self.logger.info(f"📈 Scan results: {total_opps} opportunities")
            
        except Exception as e:
            self.logger.error(f"Error in scheduled scan: {e}")
    
    async def _update_balance(self) -> float:
        """Update balance"""
        try:
            balance = await self.scalper.client.get_account_balance()
            return balance
        except Exception as e:
            self.logger.debug(f"Error updating balance: {e}")
            return self.universe.get_balance()
    
    async def _performance_snapshot(self):
        """Take performance snapshot"""
        try:
            performance = self.scalper.get_performance()
            risk_metrics = self.risk_manager.get_risk_metrics()
            current_balance = self.universe.get_balance()
            
            initial = CONFIG.INITIAL_CAPITAL
            growth_pct = ((current_balance - initial) / initial) * 100
            
            self.logger.info("💰 PERFORMANCE SNAPSHOT")
            self.logger.info(f"Account Balance: ${current_balance:.2f}")
            self.logger.info(f"Account Growth: {growth_pct:+.2f}%")
            self.logger.info(f"Total Trades: {performance['total_trades']}")
            self.logger.info(f"Win Rate: {performance['win_rate']:.1f}%")
            self.logger.info(f"Total PnL: ${performance['total_pnl']:.2f}")
            self.logger.info(f"Active Positions: {performance['active_positions']}")
            
        except Exception as e:
            self.logger.error(f"Error in performance snapshot: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, initiating shutdown...")
        asyncio.create_task(self.stop())
    
    async def stop(self):
        """Stop the bot"""
        self.logger.info("🛑 Stopping Micro Trading Bot...")
        self.is_running = False
        
        try:
            await self._performance_snapshot()
            runtime = datetime.now() - self.start_time
            self.logger.info(f"⏰ Total Runtime: {runtime}")
            self.logger.info(f"🔄 Total Iterations: {self.iteration}")
            self.logger.info("✅ Micro Trading Bot stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        finally:
            sys.exit(0)

async def main():
    """Main async entry point"""
    bot = MicroTradingBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        await bot.stop()
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())