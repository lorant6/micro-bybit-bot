#!/usr/bin/env python3
"""
Setup script for Micro Bybit Trading Bot
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}")
        print(f"Error: {e}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'config',
        'modules',
        'strategies',
        'utils',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Create .gitkeep in logs
    (Path('logs') / '.gitkeep').touch()
    print("📁 Created logs/.gitkeep")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    
    if run_command("pip install -r requirements.txt"):
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def setup_environment():
    """Setup environment configuration"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    if not env_file.exists():
        env_example.rename('.env')
        print("✅ Created .env file from example")
    else:
        print("ℹ️ .env file already exists")
    
    print("\n🔧 Please configure your .env file with:")
    print("   BYBIT_API_KEY=your_testnet_api_key_here")
    print("   BYBIT_API_SECRET=your_testnet_api_secret_here")
    print("   BYBIT_TESTNET=true")
    print("   INITIAL_CAPITAL=100")
    
    return True

def verify_setup():
    """Verify the setup completed successfully"""
    print("\n🔍 Verifying setup...")
    
    issues = []
    
    # Check required files
    required_files = [
        'main.py',
        'requirements.txt',
        'config/micro_account_config.py',
        'modules/micro_universe.py',
        'utils/micro_bybit.py'
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            issues.append(f"Missing file: {file_path}")
    
    # Check if dependencies can be imported
    try:
        import pandas
        import pybit
        print("✅ Core dependencies can be imported")
    except ImportError as e:
        issues.append(f"Dependency import error: {e}")
    
    if issues:
        print("❌ Setup issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Setup verification passed")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up Micro Bybit Trading Bot...\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Verify setup
    if not verify_setup():
        print("\n⚠️  Setup completed with warnings")
    else:
        print("\n🎉 Setup completed successfully!")
    
    print("\n📝 Next steps:")
    print("1. Edit .env file with your Bybit testnet API keys")
    print("2. Run: python run_bot.py")
    print("3. Monitor logs in logs/micro_trading.log")
    print("\n💡 Remember: Always start with TESTNET!")

if __name__ == "__main__":
    main()