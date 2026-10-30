[![Deploy to Heroku](https://img.shields.io/badge/Deploy%20to-Heroku-purple?style=for-the-badge&logo=heroku)](https://www.heroku.com/deploy?template=https://github.com/weed50gm/old_new_txt)  
# Old New TXT Bot

A Telegram bot that compares old and new text files to find new links/classes that are present in the new file but not in the old file.

## Features

- Upload old and new text files
- Compare files to find new entries
- Generate result file with new links/classes
- Admin notifications
- User-friendly interface with buttons

## Setup

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Copy the bot token you receive

### 2. Get Your Telegram User ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID

### 3. Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   export ADMIN_ID="your_telegram_user_id_here"
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Deployment

### Heroku Deployment

1. Create a Heroku account and install Heroku CLI
2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
3. Set environment variables:
   ```bash
   heroku config:set BOT_TOKEN="your_bot_token_here"
   heroku config:set ADMIN_ID="your_telegram_user_id_here"
   ```
4. Deploy:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```
5. Scale the worker:
   ```bash
   heroku ps:scale worker=1
   ```

### Render Deployment

1. Create a Render account
2. Create a new Web Service
3. Connect your GitHub repository
4. Set environment variables:
   - `BOT_TOKEN`: your bot token
   - `ADMIN_ID`: your Telegram user ID
5. Set the start command: `python bot.py`
6. Deploy

## Environment Variables

- `BOT_TOKEN`: Your Telegram bot token (required)
- `ADMIN_ID`: Your Telegram user ID for admin notifications (optional)

## Usage

1. Start the bot by sending `/start`
2. Click "Upload TXT" button
3. Upload the old text file
4. Upload the new text file
5. Wait for processing
6. Receive the result file with new links/classes

## File Format

The bot expects text files with the following format:
```
Name: Link
Another Name: Another Link
```

## License

This project is open source and available under the [MIT License](LICENSE).

