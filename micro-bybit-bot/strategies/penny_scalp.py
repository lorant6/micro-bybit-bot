"""
Penny Scalping Strategy for low-priced coins
Optimized for coins under $1
"""

def penny_scalp_signal(prices, atr):
    """
    Scalping signal for low-priced coins
    """
    if len(prices) < 20 or atr == 0:
        return 0, 'NEUTRAL'
    
    current_price = prices[-1]
    volatility = atr / current_price
    
    # High volatility scalping
    if volatility > 0.02:  # 2% volatility
        price_change = (prices[-1] - prices[-5]) / prices[-5]
        
        if price_change > 0.01:  # 1% up
            return 0.6, 'LONG'
        elif price_change < -0.01:  # 1% down
            return 0.6, 'SHORT'
    
    return 0, 'NEUTRAL'