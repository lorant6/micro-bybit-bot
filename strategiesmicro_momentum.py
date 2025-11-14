"""
Micro Momentum Strategy for $100 account
Simple momentum-based trading
"""

def calculate_momentum_signal(prices, volume):
    """
    Calculate momentum trading signal
    Returns: signal strength and direction
    """
    if len(prices) < 10:
        return 0, 'NEUTRAL'
    
    # Simple price momentum
    short_ma = sum(prices[-5:]) / 5
    long_ma = sum(prices[-10:]) / 10
    
    if short_ma > long_ma * 1.005:  # 0.5% above
        return 0.7, 'LONG'
    elif short_ma < long_ma * 0.995:  # 0.5% below
        return 0.7, 'SHORT'
    else:
        return 0, 'NEUTRAL'