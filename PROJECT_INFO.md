# Old New TXT Bot - Project Information

## Overview
This is a Telegram bot that compares old and new text files to find new links/classes that are present in the new file but not in the old file.

## Project Structure
```
├── bot.py              # Main bot application
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment configuration
├── runtime.txt        # Python version for Heroku
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── test_parser.py     # Test script for file parsing
├── deploy.py          # Deployment helper script
└── PROJECT_INFO.md    # This file
```

## Key Features
1. **Welcome Message**: Shows image and greeting with "Upload TXT" button
2. **File Upload**: Handles old and new text file uploads
3. **File Comparison**: Compares files to find new entries
4. **Result Generation**: Creates result file with new links/classes
5. **Admin Notifications**: Sends files and notifications to admin
6. **User Feedback**: Provides processing status and thank you message

## Bot Flow
1. User sends `/start` command
2. Bot shows welcome image and "Upload TXT" button
3. User clicks button and uploads old text file
4. Bot requests new text file
5. User uploads new text file
6. Bot processes files and finds differences
7. Bot sends result file to user
8. Bot sends files and notification to admin
9. Bot sends thank you message

## File Format Expected
The bot expects text files with format:
```
Name: Link
Another Name: Another Link
```

## Environment Variables
- `BOT_TOKEN`: Telegram bot token (required)
- `ADMIN_ID`: Admin Telegram user ID (optional, for notifications)

## Deployment Platforms
- **Heroku**: Use Procfile with worker dyno
- **Render**: Use Web Service with start command `python bot.py`

## Testing
Run `python test_parser.py` to test the file parsing logic locally.

## Deployment Check
Run `python deploy.py` to check if all required environment variables are set.
