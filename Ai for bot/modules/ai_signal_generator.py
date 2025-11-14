import logging
import asyncio
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

class AISignalGenerator:
    """
    AI-powered signal generator using machine learning
    Enhances traditional technical analysis with predictive models
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    async def initialize(self):
        """Initialize AI models"""
        self.logger.info("🤖 Initializing AI Signal Generator...")
        
        try:
            # Try to load pre-trained model
            self.model = await self._load_model()
            if self.model:
                self.is_trained = True
                self.logger.info("✅ Pre-trained AI model loaded")
            else:
                # Initialize new model
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42
                )
                self.logger.info("🆕 New AI model initialized (needs training)")
                
        except Exception as e:
            self.logger.error(f"Error initializing AI model: {e}")
            self.model = RandomForestClassifier(n_estimators=50, random_state=42)
    
    async def generate_ai_signals(self, symbol: str, klines: List) -> Dict:
        """Generate AI-powered trading signals"""
        try:
            if not klines or len(klines) < 50:
                return {'ai_confidence': 0, 'ai_direction': 'HOLD', 'features': {}}
            
            # Convert to DataFrame
            df = self._klines_to_dataframe(klines)
            
            # Extract features
            features = await self._extract_advanced_features(df)
            
            # Generate prediction if model is trained
            if self.is_trained:
                prediction = await self._predict_with_ai(features)
                return {
                    'ai_confidence': prediction['confidence'],
                    'ai_direction': prediction['direction'],
                    'ai_model_used': True,
                    'features': features
                }
            else:
                # Use rule-based AI as fallback
                return await self._rule_based_ai(features)
                
        except Exception as e:
            self.logger.error(f"AI signal generation error for {symbol}: {e}")
            return {'ai_confidence': 0, 'ai_direction': 'HOLD', 'features': {}}
    
    async def _extract_advanced_features(self, df: pd.DataFrame) -> Dict:
        """Extract advanced features for AI model"""
        closes = df['close'].values
        highs = df['high'].values
        lows = df['low'].values
        volumes = df['volume'].values
        
        features = {}
        
        try:
            # Price-based features
            features['price_momentum'] = (closes[-1] - closes[-5]) / closes[-5]
            features['volatility'] = np.std(closes[-20:]) / np.mean(closes[-20:])
            features['price_acceleration'] = (closes[-1] - 2*closes[-5] + closes[-10]) / closes[-10]
            
            # Volume features
            features['volume_spike'] = volumes[-1] / np.mean(volumes[-10:])
            features['volume_trend'] = np.polyfit(range(10), volumes[-10:], 1)[0]
            
            # Statistical features
            features['skewness'] = pd.Series(closes[-20:]).skew()
            features['kurtosis'] = pd.Series(closes[-20:]).kurtosis()
            
            # Market structure features
            resistance = np.max(highs[-20:])
            support = np.min(lows[-20:])
            features['price_position'] = (closes[-1] - support) / (resistance - support)
            
            # Trend strength features
            features['trend_strength'] = self._calculate_trend_strength(closes)
            features['mean_reversion'] = self._calculate_mean_reversion(closes)
            
        except Exception as e:
            self.logger.debug(f"Feature extraction error: {e}")
        
        return features
    
    async def _predict_with_ai(self, features: Dict) -> Dict:
        """Make prediction using trained AI model"""
        try:
            # Convert features to array for model
            feature_array = np.array(list(features.values())).reshape(1, -1)
            
            # Scale features
            feature_array_scaled = self.scaler.transform(feature_array)
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(feature_array_scaled)[0]
            
            # Get predicted class
            prediction = self.model.predict(feature_array_scaled)[0]
            
            confidence = np.max(probabilities)
            direction = 'LONG' if prediction == 1 else 'SHORT' if prediction == 2 else 'HOLD'
            
            return {
                'direction': direction,
                'confidence': confidence,
                'probabilities': probabilities.tolist()
            }
            
        except Exception as e:
            self.logger.error(f"AI prediction error: {e}")
            return {'direction': 'HOLD', 'confidence': 0}
    
    async def _rule_based_ai(self, features: Dict) -> Dict:
        """Rule-based AI as fallback when model isn't trained"""
        score = 0
        confidence = 0
        
        try:
            # Simple rule-based scoring
            if features.get('price_momentum', 0) > 0.02:
                score += 0.3
            if features.get('volume_spike', 0) > 1.5:
                score += 0.2
            if features.get('trend_strength', 0) > 0.6:
                score += 0.2
            if 0.3 < features.get('price_position', 0.5) < 0.7:
                score += 0.1
            if features.get('mean_reversion', 0) > 0.8:
                score -= 0.2  # Mean reversion suggests caution
            
            confidence = min(0.9, abs(score))
            direction = 'LONG' if score > 0.1 else 'SHORT' if score < -0.1 else 'HOLD'
            
            return {
                'direction': direction,
                'confidence': confidence,
                'ai_model_used': False,
                'rule_based_score': score
            }
            
        except Exception as e:
            self.logger.debug(f"Rule-based AI error: {e}")
            return {'direction': 'HOLD', 'confidence': 0}
    
    def _calculate_trend_strength(self, prices: np.ndarray) -> float:
        """Calculate trend strength using linear regression"""
        if len(prices) < 10:
            return 0
        x = np.arange(len(prices))
        slope = np.polyfit(x, prices, 1)[0]
        return abs(slope / np.mean(prices))
    
    def _calculate_mean_reversion(self, prices: np.ndarray) -> float:
        """Calculate mean reversion probability"""
        if len(prices) < 20:
            return 0
        current_price = prices[-1]
        mean_price = np.mean(prices[-20:])
        std_price = np.std(prices[-20:])
        
        if std_price == 0:
            return 0
            
        z_score = abs(current_price - mean_price) / std_price
        # Higher z-score indicates higher mean reversion probability
        return min(1.0, z_score / 3.0)
    
    async def _load_model(self):
        """Load pre-trained model (placeholder for actual model loading)"""
        # In production, you would load a saved model
        # return joblib.load('models/ai_trading_model.pkl')
        return None
    
    async def train_model(self, training_data: List[Dict]):
        """Train the AI model with new data"""
        try:
            self.logger.info("🏋️ Training AI model...")
            
            # Extract features and labels from training data
            X = []
            y = []
            
            for data_point in training_data:
                features = list(data_point['features'].values())
                label = data_point['label']  # 0: HOLD, 1: LONG, 2: SHORT
                
                X.append(features)
                y.append(label)
            
            if len(X) > 100:  # Minimum training data required
                X = np.array(X)
                y = np.array(y)
                
                # Scale features
                X_scaled = self.scaler.fit_transform(X)
                
                # Train model
                self.model.fit(X_scaled, y)
                self.is_trained = True
                
                self.logger.info(f"✅ AI model trained with {len(X)} samples")
                
                # Save model (in production)
                # joblib.dump(self.model, 'models/ai_trading_model.pkl')
                
            else:
                self.logger.warning(f"Insufficient training data: {len(X)} samples")
                
        except Exception as e:
            self.logger.error(f"AI model training error: {e}")
    
    def _klines_to_dataframe(self, klines: List) -> pd.DataFrame:
        """Convert klines to DataFrame"""
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'
        ])
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df