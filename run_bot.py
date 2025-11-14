#!/usr/bin/env python3
"""
Main entry point for Micro Bybit Trading Bot
Simplified runner with better error handling
"""

import os
import sys
import logging
import asyncio
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

async def main():
    """Main async entry point"""
    try:
        # Import and run the bot
        from main import MicroTradingBot
        
        print("💰 Micro Bybit Trading Bot - $100 Account")
        print("=" * 50)
        
        # Check environment variables
        required_vars = ['BYBIT_API_KEY', 'BYBIT_API_SECRET']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            print("💡 Please set them in your .env file or environment")
            sys.exit(1)
        
        # Initialize and run bot
        bot = MicroTradingBot()
        await bot.start()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.exception("Fatal error in main")
        sys.exit(1)

if __name__ == "__main__":
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the bot
    asyncio.run(main())