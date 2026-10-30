#!/usr/bin/env python3
"""
Deployment helper script
"""

import os
import sys

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['BOT_TOKEN', 'ADMIN_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables before running the bot.")
        return False
    
    print("✅ All required environment variables are set.")
    return True

def main():
    """Main deployment check function."""
    print("🤖 Old New TXT Bot - Deployment Check")
    print("=" * 40)
    
    if not check_environment():
        sys.exit(1)
    
    print("\n🚀 Ready to deploy!")
    print("\nFor Heroku deployment:")
    print("1. heroku create your-app-name")
    print("2. heroku config:set BOT_TOKEN=your_token")
    print("3. heroku config:set ADMIN_ID=your_user_id")
    print("4. git push heroku main")
    print("5. heroku ps:scale worker=1")
    
    print("\nFor Render deployment:")
    print("1. Create new Web Service")
    print("2. Connect GitHub repository")
    print("3. Set environment variables")
    print("4. Set start command: python bot.py")
    print("5. Deploy")

if __name__ == "__main__":
    main()
