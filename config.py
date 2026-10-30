import os

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Validate required environment variables
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")

if not ADMIN_ID:
    print("Warning: ADMIN_ID not set. Admin notifications will be disabled.")
