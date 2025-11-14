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
from modules.ai_risk_manager import AIRiskManager  # Add AI risk manager
# AI modules would be automatically imported through the enhanced scanner

class MicroTradingBot:
    """Micro Trading Bot with AI enhancements"""
    
    def __init__(self):
        MicroLogger.setup()
        self.logger = logging.getLogger(__name__)
        
        # Initialize modules
        self.universe = MicroUniverseManager()
        self.risk_manager = NanoRiskManager()
        self.ai_risk_manager = AIRiskManager(self.risk_manager)  # AI risk layer
        self.scanner = EfficientScanner(self.universe)
        self.scalper = MicroScalpingEngine(self.risk_manager)
        
        # Bot state
        self.is_running = False
        self.start_time = None
        self.iteration = 0
        
        # AI performance tracking
        self.ai_performance = {
            'ai_signals_used': 0,
            'ai_signals_profitable': 0,
            'traditional_signals_used': 0,
            'traditional_signals_profitable': 0
        }
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    async def start(self):
        """Start the AI-enhanced bot"""
        self.logger.info("🧠 Starting AI-Enhanced Trading Bot - $100 Account")
        self.is_running = True
        self.start_time = datetime.now()
        
        try:
            await self._initialize_system()
            await self._ai_trading_loop()
        except Exception as e:
            self.logger.critical(f"Critical error: {e}")
            await self.stop()
    
    async def _initialize_system(self):
        """Initialize AI-enhanced system"""
        self.logger.info("Initializing AI trading system...")
        
        await self.universe.initialize()
        await self.risk_manager.initialize()
        await self.scanner.quick_scan()  # This now initializes AI components
        
        self.logger.info("✅ AI trading system initialized")
        self.logger.info(f"🎯 Trading with: ${CONFIG.INITIAL_CAPITAL}")
        self.logger.info(f"📊 Monitoring: {len(self.universe.active_symbols)} symbols")
        self.logger.info("🤖 AI Features: Signal Generation, Risk Management")
    
    async def _ai_trading_loop(self):
        """Main AI trading loop"""
        self.logger.info("Entering AI trading loop...")
        
        while self.is_running:
            try:
                self.iteration += 1
                
                # Monitor active positions
                await self.scalper.monitor_micro_positions()
                
                # Update balance
                current_balance = await self._update_balance()
                self.universe.update_balance(current_balance)
                
                # AI Market Analysis
                market_data = await self._collect_market_data()
                risk_analysis = await self.ai_risk_manager.analyze_market_conditions(market_data)
                
                # Check if trading is allowed with AI risk assessment
                if not self.risk_manager.can_trade() or risk_analysis['market_regime'] == 'CRASH':
                    self.logger.warning(f"🚨 Trading paused - {risk_analysis['market_regime']} regime")
                    await asyncio.sleep(30)
                    continue
                
                # Scheduled operations
                await self._execute_ai_operations(risk_analysis)
                
                # AI Performance snapshot
                if self.iteration % 60 == 0:
                    await self._ai_performance_snapshot(risk_analysis)
                
                await asyncio.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error in AI iteration {self.iteration}: {e}")
                await asyncio.sleep(10)
    
    async def _execute_ai_operations(self, risk_analysis: Dict):
        """Execute AI-enhanced operations"""
        if self.iteration % 60 == 0:
            await self._ai_enhanced_scan_and_trade(risk_analysis)
        
        if self.iteration % 2880 == 0:
            self.risk_manager.reset_daily_metrics()
            self.logger.info("🔄 Daily risk metrics reset")
    
    async def _ai_enhanced_scan_and_trade(self, risk_analysis: Dict):
        """AI-enhanced scanning and trading"""
        self.logger.info("🤖 Executing AI-enhanced scan...")
        
        try:
            # Perform AI-enhanced scan
            opportunities = await self.scanner.quick_scan()
            
            # Get top opportunities including AI signals
            top_opps = self.scanner.get_top_opportunities(limit=5)  # Get more for AI filtering
            
            # AI risk filtering
            filtered_opps = await self._ai_risk_filter(top_opps, risk_analysis)
            
            # Execute trades with AI-adjusted position sizes
            if filtered_opps:
                await self._execute_ai_trades(filtered_opps, risk_analysis)
            
            # Log AI performance
            ai_opps = [opp for opp in filtered_opps if opp.get('ai_enhanced') or opp.get('type') == 'ai_signal']
            traditional_opps = [opp for opp in filtered_opps if not opp.get('ai_enhanced')]
            
            self.logger.info(f"📈 AI Scan: {len(filtered_opps)} opportunities "
                           f"({len(ai_opps)} AI, {len(traditional_opps)} traditional)")
            
        except Exception as e:
            self.logger.error(f"Error in AI-enhanced scan: {e}")
    
    async def _ai_risk_filter(self, opportunities: List[Dict], risk_analysis: Dict) -> List[Dict]:
        """Filter opportunities using AI risk assessment"""
        filtered = []
        
        for opp in opportunities:
            try:
                # Skip if market regime is volatile and opportunity is high-risk
                if (risk_analysis['market_regime'] == 'VOLATILE' and 
                    opp.get('score', 0) < 0.8):  # Higher threshold in volatile markets
                    continue
                
                # Adjust position size based on AI risk
                original_size = self.scalper._calculate_micro_position_size(
                    opp['symbol'], opp['current_price']
                )
                
                ai_adjusted_size = await self.ai_risk_manager.get_ai_risk_adjustment(
                    opp['symbol'], original_size
                )
                
                if ai_adjusted_size > 0:
                    opp['ai_adjusted_size'] = ai_adjusted_size
                    filtered.append(opp)
                    
            except Exception as e:
                self.logger.debug(f"AI risk filter error for {opp['symbol']}: {e}")
                filtered.append(opp)  # Include anyway as fallback
        
        return filtered
    
    async def _execute_ai_trades(self, opportunities: List[Dict], risk_analysis: Dict):
        """Execute trades with AI enhancements"""
        for opportunity in opportunities:
            try:
                # Use AI-adjusted position size if available
                if 'ai_adjusted_size' in opportunity:
                    # We need to modify the scalper to accept custom position sizes
                    # This would require updates to the scalper module
                    pass
                
                # Track AI vs traditional performance
                if opportunity.get('ai_enhanced') or opportunity.get('type') == 'ai_signal':
                    self.ai_performance['ai_signals_used'] += 1
                else:
                    self.ai_performance['traditional_signals_used'] += 1
                    
            except Exception as e:
                self.logger.error(f"AI trade execution error: {e}")
    
    async def _collect_market_data(self) -> Dict:
        """Collect market data for AI analysis"""
        # Simplified market data collection
        # In production, you would collect more comprehensive data
        market_data = {}
        
        symbols = self.universe.get_tradable_symbols()[:10]  # Sample of symbols
        
        for symbol in symbols:
            try:
                ticker = await self.scalper.client.get_ticker(symbol)
                if ticker:
                    market_data[symbol] = {
                        'price': float(ticker.get('lastPrice', 0)),
                        'volume': float(ticker.get('volume24h', 0)),
                        'price_change': float(ticker.get('price24hPcnt', 0))
                    }
            except Exception as e:
                self.logger.debug(f"Market data collection error for {symbol}: {e}")
        
        return market_data
    
    async def _ai_performance_snapshot(self, risk_analysis: Dict):
        """Take AI performance snapshot"""
        try:
            performance = self.scalper.get_performance()
            risk_metrics = self.risk_manager.get_risk_metrics()
            current_balance = self.universe.get_balance()
            
            initial = CONFIG.INITIAL_CAPITAL
            growth_pct = ((current_balance - initial) / initial) * 100
            
            # Calculate AI performance metrics
            ai_success_rate = 0
            if self.ai_performance['ai_signals_used'] > 0:
                ai_success_rate = (self.ai_performance['ai_signals_profitable'] / 
                                 self.ai_performance['ai_signals_used']) * 100
            
            self.logger.info("🧠 AI PERFORMANCE SNAPSHOT")
            self.logger.info(f"Account Balance: ${current_balance:.2f}")
            self.logger.info(f"Account Growth: {growth_pct:+.2f}%")
            self.logger.info(f"Market Regime: {risk_analysis['market_regime']}")
            self.logger.info(f"AI Risk Multiplier: {risk_analysis['risk_multiplier']}")
            self.logger.info(f"AI Signals Used: {self.ai_performance['ai_signals_used']}")
            self.logger.info(f"AI Success Rate: {ai_success_rate:.1f}%")
            self.logger.info(f"Traditional Signals: {self.ai_performance['traditional_signals_used']}")
            self.logger.info(f"Total Trades: {performance['total_trades']}")
            self.logger.info(f"Win Rate: {performance['win_rate']:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Error in AI performance snapshot: {e}")
    
    # Keep existing methods for balance update and signal handling
    async def _update_balance(self) -> float:
        """Update balance"""
        try:
            balance = await self.scalper.client.get_account_balance()
            return balance
        except Exception as e:
            self.logger.debug(f"Error updating balance: {e}")
            return self.universe.get_balance()
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {signum}, initiating AI shutdown...")
        asyncio.create_task(self.stop())
    
    async def stop(self):
        """Stop the AI-enhanced bot"""
        self.logger.info("🛑 Stopping AI Trading Bot...")
        self.is_running = False
        
        try:
            # Final AI performance report
            risk_analysis = await self.ai_risk_manager.analyze_market_conditions({})
            await self._ai_performance_snapshot(risk_analysis)
            
            runtime = datetime.now() - self.start_time
            self.logger.info(f"⏰ Total Runtime: {runtime}")
            self.logger.info(f"🔄 Total Iterations: {self.iteration}")
            self.logger.info("✅ AI Trading Bot stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error during AI shutdown: {e}")
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