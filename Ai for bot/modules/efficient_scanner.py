import asyncio
import logging
import pandas as pd
from typing import Dict, List
from utils.micro_bybit import MicroBybitClient
from utils.efficient_indicators import EfficientIndicators
from modules.micro_universe import MicroUniverseManager
from modules.ai_signal_generator import AISignalGenerator  # Add this import
from config.micro_account_config import CONFIG

class EfficientScanner:
    """Efficient scanner enhanced with AI capabilities"""
    
    def __init__(self, universe_manager: MicroUniverseManager):
        self.universe = universe_manager
        self.client = MicroBybitClient()
        self.indicators = EfficientIndicators()
        self.ai_generator = AISignalGenerator()  # Add AI component
        self.logger = logging.getLogger(__name__)
        
        self.scan_results = {}
        self.last_scan_time = None
    
    async def quick_scan(self) -> Dict[str, List]:
        """Perform AI-enhanced quick scan"""
        self.logger.info("🔍 Performing AI-enhanced quick scan...")
        
        # Initialize AI if not already done
        await self.ai_generator.initialize()
        
        symbols = self.universe.get_symbols_by_volume(CONFIG.MIN_24H_VOLUME)
        symbols = symbols[:CONFIG.MAX_SYMBOLS_TO_SCAN]
        
        opportunities = {'momentum': [], 'reversal': [], 'breakout': [], 'ai_signals': []}
        
        batch_size = 10
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            batch_opps = await self._process_batch_with_ai(batch)  # Updated method
            
            for key in opportunities.keys():
                opportunities[key].extend(batch_opps.get(key, []))
            
            await asyncio.sleep(1)
        
        # Filter and rank opportunities
        for key in opportunities.keys():
            opportunities[key] = sorted(
                [opp for opp in opportunities[key] if opp['score'] > 0.6],
                key=lambda x: x['score'],
                reverse=True
            )[:5]
        
        self.scan_results = opportunities
        self.last_scan_time = pd.Timestamp.now()
        
        total_opps = sum(len(opps) for opps in opportunities.values())
        ai_opps = len(opportunities['ai_signals'])
        self.logger.info(f"✅ AI scan complete: {total_opps} opportunities ({ai_opps} AI signals)")
        
        return opportunities
    
    async def _process_batch_with_ai(self, symbols: List[str]) -> Dict[str, List]:
        """Process batch with AI enhancement"""
        opportunities = {'momentum': [], 'reversal': [], 'breakout': [], 'ai_signals': []}
        
        for symbol in symbols:
            try:
                klines = await self.client.get_klines(symbol, '5m', 100)  # Get more data for AI
                if not klines or len(klines) < 50:
                    continue
                
                df = self._klines_to_dataframe(klines)
                closes = df['close'].values
                highs = df['high'].values
                lows = df['low'].values
                current_price = closes[-1]
                
                # Traditional analysis
                analysis = self._quick_analysis(closes, highs, lows, current_price)
                
                # AI analysis
                ai_signals = await self.ai_generator.generate_ai_signals(symbol, klines)
                
                # Generate opportunities combining both
                symbol_opps = self._generate_ai_enhanced_opportunities(
                    symbol, analysis, ai_signals, current_price
                )
                
                for opp_type, opp_data in symbol_opps.items():
                    if opp_data:
                        opportunities[opp_type].append(opp_data)
                        
            except Exception as e:
                self.logger.debug(f"Error processing {symbol}: {e}")
        
        return opportunities
    
    def _generate_ai_enhanced_opportunities(self, symbol: str, analysis: Dict, 
                                          ai_signals: Dict, current_price: float) -> Dict[str, Dict]:
        """Generate AI-enhanced trading opportunities"""
        opportunities = {}
        
        # Traditional momentum opportunity
        momentum_score = self._calculate_momentum_score(analysis, current_price)
        
        # AI-enhanced momentum
        if ai_signals['ai_direction'] == 'LONG' and ai_signals['ai_confidence'] > 0.7:
            momentum_score = min(1.0, momentum_score + ai_signals['ai_confidence'] * 0.3)
        elif ai_signals['ai_direction'] == 'SHORT' and ai_signals['ai_confidence'] > 0.7:
            momentum_score = max(-1.0, momentum_score - ai_signals['ai_confidence'] * 0.3)
        
        if abs(momentum_score) > 0.6:
            opportunities['momentum'] = {
                'symbol': symbol,
                'score': abs(momentum_score),
                'direction': 'LONG' if momentum_score > 0 else 'SHORT',
                'current_price': current_price,
                'type': 'momentum',
                'ai_enhanced': True,
                'ai_confidence': ai_signals.get('ai_confidence', 0)
            }
        
        # Pure AI signals (high confidence)
        if ai_signals['ai_confidence'] > 0.8 and ai_signals['ai_direction'] != 'HOLD':
            opportunities['ai_signals'] = {
                'symbol': symbol,
                'score': ai_signals['ai_confidence'],
                'direction': ai_signals['ai_direction'],
                'current_price': current_price,
                'type': 'ai_signal',
                'ai_model_used': ai_signals.get('ai_model_used', False),
                'confidence': ai_signals['ai_confidence']
            }
        
        # Reversal opportunity with AI confirmation
        reversal_score = self._calculate_reversal_score(analysis, current_price)
        if reversal_score > 0.65 and ai_signals['ai_confidence'] > 0.6:
            opportunities['reversal'] = {
                'symbol': symbol,
                'score': reversal_score,
                'direction': 'LONG' if analysis['rsi'] < 30 else 'SHORT',
                'current_price': current_price,
                'type': 'reversal',
                'ai_confirmed': True
            }
        
        return opportunities
    
    # Keep existing helper methods (_quick_analysis, _calculate_momentum_score, etc.)
    def _quick_analysis(self, closes: List[float], highs: List[float], 
                       lows: List[float], current_price: float) -> Dict:
        """Quick technical analysis"""
        analysis = {}
        
        try:
            analysis['rsi'] = self.indicators.rsi(closes, 14)
            analysis['ema_8'] = self.indicators.ema(closes, 8)
            analysis['ema_21'] = self.indicators.ema(closes, 21)
            analysis['atr'] = self.indicators.atr(highs, lows, closes, 14)
            analysis['momentum_5'] = (closes[-1] - closes[-5]) / closes[-5]
            analysis['resistance'] = max(highs[-10:])
            analysis['support'] = min(lows[-10:])
        except Exception as e:
            self.logger.debug(f"Error in quick analysis: {e}")
        
        return analysis
    
    def _calculate_momentum_score(self, analysis: Dict, current_price: float) -> float:
        """Calculate momentum score"""
        if not all(k in analysis for k in ['rsi', 'ema_8', 'ema_21', 'momentum_5']):
            return 0
        
        score = 0
        
        if analysis['ema_8'] > analysis['ema_21']:
            score += 0.3
        else:
            score -= 0.3
        
        if 40 < analysis['rsi'] < 70:
            score += 0.2
        elif analysis['rsi'] > 70:
            score -= 0.2
        
        if analysis['momentum_5'] > 0.01:
            score += 0.3
        elif analysis['momentum_5'] < -0.01:
            score -= 0.3
        
        return max(-1, min(1, score))
    
    def _calculate_reversal_score(self, analysis: Dict, current_price: float) -> float:
        """Calculate reversal score"""
        if 'rsi' not in analysis:
            return 0
        
        score = 0
        
        if analysis['rsi'] < 30:
            score += 0.6
        elif analysis['rsi'] > 70:
            score += 0.6
        
        if current_price <= analysis.get('support', current_price) * 1.01:
            score += 0.2
        
        return min(1, score)
    
    def _klines_to_dataframe(self, klines: List) -> pd.DataFrame:
        """Convert klines to DataFrame"""
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'
        ])
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def get_top_opportunities(self, limit: int = 3) -> List[Dict]:
        """Get top opportunities including AI signals"""
        all_opps = []
        for category in self.scan_results.values():
            all_opps.extend(category)
        
        return sorted(all_opps, key=lambda x: x['score'], reverse=True)[:limit]