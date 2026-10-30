import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import asyncio
from io import StringIO
import re
from config import BOT_TOKEN, ADMIN_ID

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User states
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_states[user.id] = {'step': 'idle'}
    
    # Create inline keyboard with Upload TXT button
    keyboard = [[InlineKeyboardButton("Upload TXT", callback_data='upload_txt')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send welcome message with image
    welcome_text = f"Hello {user.first_name}! This is an old new txt bot. You can simply upload old and new txt files to get the new links/classes."
    
    await update.message.reply_photo(
        photo='https://i.ibb.co/zTPJFct8/photo-2025-04-25-12-55-01-7497233558289776672.jpg',
        caption=welcome_text,
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'upload_txt':
        user_id = query.from_user.id
        user_states[user_id] = {'step': 'waiting_old_txt'}
        
        # Check if the message has a caption (photo message) or is a text message
        if query.message.caption:
            # It's a photo message, edit the caption
            await query.edit_message_caption(
                caption="Please upload the OLD txt file:",
                reply_markup=None
            )
        else:
            # It's a text message, edit the text
            await query.edit_message_text("Please upload the OLD txt file:")
        
        # Store the message ID for later deletion
        user_states[user_id]['bot_message_id'] = query.message.message_id

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document uploads."""
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        user_states[user_id] = {'step': 'idle'}
    
    current_step = user_states[user_id].get('step', 'idle')
    
    if current_step == 'waiting_old_txt':
        # Delete the user's uploaded file message
        try:
            await asyncio.sleep(0.5)  # Small delay to ensure message is processed
            await context.bot.delete_message(chat_id=user_id, message_id=update.message.message_id)
        except Exception as e:
            logger.warning(f"Could not delete user message: {e}")
        
        # Download old txt file
        file = await context.bot.get_file(update.message.document.file_id)
        old_content = await file.download_as_bytearray()
        old_text = old_content.decode('utf-8')
        
        user_states[user_id] = {
            'step': 'waiting_new_txt',
            'old_txt': old_text,
            'old_filename': update.message.document.file_name,
            'bot_message_id': user_states[user_id].get('bot_message_id')
        }
        
        # Edit the bot's previous message to ask for new file
        bot_message_id = user_states[user_id].get('bot_message_id')
        if bot_message_id:
            try:
                await context.bot.edit_message_caption(
                    chat_id=user_id,
                    message_id=bot_message_id,
                    caption="Upload New TXT"
                )
            except Exception as e:
                logger.warning(f"Could not edit bot message: {e}")
                # Send new message if edit fails
                new_msg = await context.bot.send_message(user_id, "Upload New TXT")
                user_states[user_id]['bot_message_id'] = new_msg.message_id
        
    elif current_step == 'waiting_new_txt':
        # Delete the user's uploaded file message
        try:
            await asyncio.sleep(0.5)  # Small delay to ensure message is processed
            await context.bot.delete_message(chat_id=user_id, message_id=update.message.message_id)
        except Exception as e:
            logger.warning(f"Could not delete user message: {e}")
        
        # Download new txt file
        file = await context.bot.get_file(update.message.document.file_id)
        new_content = await file.download_as_bytearray()
        new_text = new_content.decode('utf-8')
        
        user_states[user_id]['new_txt'] = new_text
        user_states[user_id]['new_filename'] = update.message.document.file_name
        user_states[user_id]['step'] = 'processing'
        
        # Edit the bot's previous message to show processing
        bot_message_id = user_states[user_id].get('bot_message_id')
        if bot_message_id:
            try:
                await context.bot.edit_message_caption(
                    chat_id=user_id,
                    message_id=bot_message_id,
                    caption="Processing..."
                )
            except Exception as e:
                logger.warning(f"Could not edit bot message: {e}")
                # Send new message if edit fails
                await context.bot.send_message(user_id, "Processing...")
        
        # Process files
        await process_files(update, context, user_id)
    else:
        await update.message.reply_text("Please use the /start command first.")

async def process_files(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    """Process the old and new txt files to find differences."""
    try:
        user_data = user_states[user_id]
        old_txt = user_data['old_txt']
        new_txt = user_data['new_txt']
        new_filename = user_data['new_filename']
        
        # Parse old file to extract links and names
        old_entries = parse_txt_file(old_txt)
        
        # Parse new file to extract links and names
        new_entries = parse_txt_file(new_txt)
        
        # Find entries that are in new but not in old
        old_links = {entry['link'] for entry in old_entries}
        old_names = {entry['name'] for entry in old_entries}
        
        new_only_entries = []
        for entry in new_entries:
            if entry['link'] not in old_links and entry['name'] not in old_names:
                new_only_entries.append(entry)
        
        # Create result file
        result_content = create_result_file(new_only_entries)
        
        # Send result file to user
        result_filename = f"new_{new_filename}"
        await context.bot.send_document(
            chat_id=user_id,
            document=StringIO(result_content),
            filename=result_filename,
            caption="Here are the new links/classes that were not in the old file:"
        )
        
        # Send admin notification
        if ADMIN_ID:
            admin_message = f"User {update.effective_user.first_name} ({update.effective_user.username or 'No username'}) uploaded files:\n"
            admin_message += f"Old file: {user_data['old_filename']}\n"
            admin_message += f"New file: {new_filename}\n"
            admin_message += f"Found {len(new_only_entries)} new entries."
            
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
            
            # Send files to admin
            await context.bot.send_document(
                chat_id=ADMIN_ID,
                document=StringIO(old_txt),
                filename=user_data['old_filename']
            )
            await context.bot.send_document(
                chat_id=ADMIN_ID,
                document=StringIO(new_txt),
                filename=new_filename
            )
            await context.bot.send_document(
                chat_id=ADMIN_ID,
                document=StringIO(result_content),
                filename=result_filename
            )
        
        # Delete the processing message
        bot_message_id = user_states[user_id].get('bot_message_id')
        if bot_message_id:
            try:
                await context.bot.delete_message(chat_id=user_id, message_id=bot_message_id)
            except Exception as e:
                logger.warning(f"Could not delete processing message: {e}")
        
        # Thank you message
        await context.bot.send_message(
            chat_id=user_id,
            text="Thank you! The processing is complete."
        )
        
        # Reset user state
        user_states[user_id] = {'step': 'idle'}
        
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text="Sorry, there was an error processing your files. Please try again."
        )
        user_states[user_id] = {'step': 'idle'}

def parse_txt_file(content: str) -> list:
    """Parse txt file content to extract names and links."""
    entries = []
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line and ':' in line:
            # Split by first colon to separate name and link
            parts = line.split(':', 1)
            if len(parts) == 2:
                name = parts[0].strip()
                link = parts[1].strip()
                if name and link:
                    entries.append({
                        'name': name,
                        'link': link,
                        'original_line': line
                    })
    
    return entries

def create_result_file(entries: list) -> str:
    """Create result file content from entries."""
    if not entries:
        return "No new entries found."
    
    result_lines = []
    for entry in entries:
        result_lines.append(entry['original_line'])
    
    return '\n'.join(result_lines)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, something went wrong. Please try again or contact the admin."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.TEXT, handle_document))
    application.add_error_handler(error_handler)
    
    # Run the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
