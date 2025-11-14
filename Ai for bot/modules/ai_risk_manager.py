import logging
import numpy as np
from typing import Dict, List
from config.micro_account_config import CONFIG

class AIRiskManager:
    """
    AI-enhanced risk management
    Uses machine learning to predict market conditions and adjust risk
    """
    
    def __init__(self, base_risk_manager):
        self.base_risk = base_risk_manager
        self.logger = logging.getLogger(__name__)
        
        # AI risk parameters
        self.market_regime = "NORMAL"  # NORMAL, VOLATILE, CRASH
        self.risk_multiplier = 1.0
        self.volatility_forecast = 0.0
        
    async def analyze_market_conditions(self, market_data: Dict) -> Dict:
        """Analyze current market conditions using AI"""
        try:
            # Calculate market volatility
            volatility = await self._calculate_market_volatility(market_data)
            self.volatility_forecast = volatility
            
            # Determine market regime
            if volatility > 0.08:  # 8% volatility
                self.market_regime = "VOLATILE"
                self.risk_multiplier = 0.5  # Reduce risk by 50%
            elif volatility > 0.15:  # 15% volatility
                self.market_regime = "CRASH"
                self.risk_multiplier = 0.2  # Reduce risk by 80%
            else:
                self.market_regime = "NORMAL"
                self.risk_multiplier = 1.0
            
            # AI-based correlation analysis
            correlation_risk = await self._analyze_correlation_risk(market_data)
            
            return {
                'market_regime': self.market_regime,
                'risk_multiplier': self.risk_multiplier,
                'volatility_forecast': volatility,
                'correlation_risk': correlation_risk,
                'recommended_position_size': self._calculate_ai_position_size()
            }
            
        except Exception as e:
            self.logger.error(f"AI risk analysis error: {e}")
            return {
                'market_regime': 'NORMAL',
                'risk_multiplier': 1.0,
                'volatility_forecast': 0.0,
                'correlation_risk': 'LOW',
                'recommended_position_size': CONFIG.MAX_POSITION_SIZE
            }
    
    async def get_ai_risk_adjustment(self, symbol: str, position_size: float) -> float:
        """Get AI-adjusted position size"""
        try:
            base_approval = self.base_risk.approve_trade(symbol, position_size, 0, 0)
            
            if not base_approval:
                return 0
            
            # Apply AI risk multiplier
            ai_adjusted_size = position_size * self.risk_multiplier
            
            # Ensure minimum position size
            ai_adjusted_size = max(CONFIG.MIN_POSITION_SIZE, ai_adjusted_size)
            
            self.logger.info(f"🤖 AI Risk: {self.market_regime} regime, "
                           f"position size adjusted to ${ai_adjusted_size:.2f}")
            
            return ai_adjusted_size
            
        except Exception as e:
            self.logger.error(f"AI risk adjustment error: {e}")
            return position_size  # Fallback to original size
    
    async def _calculate_market_volatility(self, market_data: Dict) -> float:
        """Calculate current market volatility"""
        try:
            # Simple volatility calculation (replace with more sophisticated AI)
            price_changes = []
            for symbol_data in market_data.values():
                if 'price_changes' in symbol_data:
                    price_changes.extend(symbol_data['price_changes'])
            
            if price_changes:
                return np.std(price_changes)
            else:
                return 0.05  # Default 5% volatility
        
        except Exception as e:
            self.logger.debug(f"Volatility calculation error: {e}")
            return 0.05
    
    async def _analyze_correlation_risk(self, market_data: Dict) -> str:
        """Analyze correlation risk between positions"""
        try:
            # Simple correlation analysis
            if len(market_data) < 2:
                return "LOW"
            
            # Count similar positions
            long_positions = sum(1 for data in market_data.values() 
                               if data.get('signal') == 'LONG')
            short_positions = sum(1 for data in market_data.values() 
                                if data.get('signal') == 'SHORT')
            
            total_positions = long_positions + short_positions
            
            if total_positions == 0:
                return "LOW"
            
            # High correlation if most positions are in same direction
            max_direction = max(long_positions, short_positions)
            correlation_ratio = max_direction / total_positions
            
            if correlation_ratio > 0.8:
                return "HIGH"
            elif correlation_ratio > 0.6:
                return "MEDIUM"
            else:
                return "LOW"
                
        except Exception as e:
            self.logger.debug(f"Correlation analysis error: {e}")
            return "LOW"
    
    def _calculate_ai_position_size(self) -> float:
        """Calculate AI-recommended position size"""
        base_size = CONFIG.MAX_POSITION_SIZE
        return base_size * self.risk_multiplier
    
    def should_reduce_exposure(self) -> bool:
        """Determine if portfolio exposure should be reduced"""
        return self.market_regime in ["VOLATILE", "CRASH"]
    
    def get_risk_summary(self) -> Dict:
        """Get AI risk management summary"""
        return {
            'market_regime': self.market_regime,
            'risk_multiplier': self.risk_multiplier,
            'volatility_forecast': self.volatility_forecast,
            'recommended_action': 'REDUCE_EXPOSURE' if self.should_reduce_exposure() else 'NORMAL'
        }