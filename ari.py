import random
import asyncio
import logging
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ChatPermissions
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime, timedelta
from database import (
    add_sudo, remove_sudo, list_sudo_users, is_sudo_user,
    add_exempt_user, remove_exempt_user, list_exempt_users,
    add_muted_user, remove_muted_user, is_muted_user
)

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Bot Token & Owner ID
OWNER_USER_ID = 7875192045  # Replace with your Telegram ID

# List of video file URLs to send randomly
VIDEO_LIST = [
    "https://telegra.ph/file/1722b8e21ef54ef4fbc23.mp4",
    "https://telegra.ph/file/ac7186fffc5ac5f764fc1.mp4",
    "https://telegra.ph/file/4156557a73657501918c4.mp4",
    "https://telegra.ph/file/0d896710f1f1c02ad2549.mp4",
    "https://telegra.ph/file/03ac4a6e94b5b4401fa5a.mp4",
]

# Set a maximum length for messages
MAX_MESSAGE_LENGTH = 200

# Function to create the main inline keyboard
def get_main_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("‣ʜᴇʟᴘ‣", callback_data="help"),
            InlineKeyboardButton("‣ᴀᴅᴅ ᴍᴇ‣", url="https://t.me/copyright_ro_bot?startgroup=true"),
        ],
        [
            InlineKeyboardButton("‣ꜱᴜᴘᴘᴏʀᴛ‣", url="https://t.me/love_mhe"),
            InlineKeyboardButton("‣ᴏᴡɴᴇʀ‣", url="https://t.me/xazoc"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to create the "Back" button to return to the main menu
def get_back_inline_keyboard():
    keyboard = [[InlineKeyboardButton("‣ʙᴀᴄᴋ‣", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

# Function to check if a user is exempt from deletion
def is_exempt_user(user_id: int) -> bool:
    return user_id == OWNER_USER_ID or is_sudo_user(user_id)

# Handler for the /start command
async def start_command(update: Update, context):
    message = update.message

    # Step 1: Animate the message "dιиg dιиg"
    accha = await message.reply_text(
        text="❤️‍🔥ᴅιиg ᴅιиg ꨄ︎ ѕтαятιиg••"
    )
    await asyncio.sleep(0.2)
    await accha.edit_text("💛ᴅιиg ᴅιиg ꨄ︎ sтαятιиg•••")
    await asyncio.sleep(0.2)
    await accha.edit_text("🩵ᴅιиg ᴅιиg ꨄ︎ sтαятιиg•••••")
    await asyncio.sleep(0.2)
    await accha.edit_text("🤍ᴅιиg ᴅιиg ꨄ︎ sтαятιиg••••••••")
    await asyncio.sleep(0.2)
    await accha.delete()

    # Step 2: Select a random video from the VIDEO_LIST
    video_url = random.choice(VIDEO_LIST)

    # Step 3: Prepare the final message caption
    caption = (
        f"╭────────────────────── \n"
        f"╰──●нυι тнιѕ ιѕ ˹𝑪𝒐𝒑𝒚𝒓𝒊𝒈𝒉𝒕 ✗ 𝜝𝒐𝒕˼🤍\n\n"
        f"ғʀᴏм ᴄᴏᴘyʀιɢнт ᴘʀᴏтᴇcтιᴏɴ тᴏ ᴍᴀιɴтᴀιɴιɴɢ ᴅᴇcᴏʀυм, ᴡᴇ'vᴇ ɢᴏт ιт cᴏvᴇʀᴇᴅ. 🌙\n\n"
        f"●ɴᴏ cᴏммᴀɴᴅ, ᴊᴜѕт ᴀᴅᴅ тнιѕ ʙᴏᴛ, ᴇvᴇʀyтнιɴɢ ιѕ ᴀυтᴏ 🍁\n\n"
        f"⋆━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ\n"
        f"ᴍᴀᴅᴇ ᴡιтн 🖤 ʙy @xazoc❣️"
    )

    # Step 4: Send the video with the caption and inline keyboard
    await message.reply_video(
        video=video_url,
        caption=caption,
        parse_mode="HTML",
        reply_markup=get_main_inline_keyboard()
    )

# Handler for button presses
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        help_text = (
            "💫Here are some commands:\n\n"
            "● [/start] - Start the bot\n"
            "● This bot automatically deletes edited messages, long messages, and shared links or PDFs.🍃\n"
            "● If you want to add a new video, send it to @xazoc.🤍\n"
            "● If you need any kind of help, DM @xotikop_bot🩵\n"
            "● If you want to add yourself in sudo, contact @xazoc.💛\n\n"
            "#𝐒ᴀфᴇ ᴇᴄᴏ🍃 , #𝐗ᴏᴛɪᴋ❤️‍🔥"
        )
        await query.message.edit_caption(help_text, reply_markup=get_back_inline_keyboard())

    elif query.data == "back":
        video_url = random.choice(VIDEO_LIST)
        caption = (
            f"╭────────────────────── \n"
            f"╰──●нυι тнιѕ ιѕ ˹𝑪𝒐𝒑𝒚𝒓𝒊𝒈𝒉𝒕 ✗ 𝜝𝒐𝒛˼🤍\n\n"
            f"ғʀᴏм ᴄᴏᴘyʀιɢнт ᴘʀᴏтᴇcтιᴏɴ тᴏ ᴍᴀιɴтᴀιɴιɴɢ ᴅᴇcᴏʀυм, ᴡᴇ'vᴇ ɢᴏт ιт cᴏvᴇʀᴇᴅ. 🌙\n\n"
            f"●ɴᴏ cᴏммᴀɴᴅ, ᴊᴜѕт ᴀᴅᴅ тнιѕ ʙᴏᴛ, ᴇvᴇʀyтнιɴɢ ιѕ ᴀυтᴏ 🍁\n\n"
            f"⋆━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ┄ׅ━ׄ\n"
            f"ᴍᴀᴅᴇ ᴡιтн 🖤 ʙy @xazoc❣️"
        )
        await query.message.edit_caption(caption, reply_markup=get_main_inline_keyboard())

# /addsudo Command (Owner Only)
async def addsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_USER_ID:
        logger.warning(f"Unauthorized access attempt by {update.message.from_user.id}")
        return await update.message.reply_text("❌ You are not authorized!")
    
    try:
        user_input = context.args[0] if context.args else None
        resolved_user_id = await resolve_user(context, update, user_input)

        if not resolved_user_id:
            return await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")

        add_sudo(resolved_user_id)
        await update.message.reply_text(f"✅ User {resolved_user_id} added as sudo!")
    except Exception as e:
        logger.error(f"Error adding sudo user: {e}")
        await update.message.reply_text("❌ Failed to add sudo user. Please check the input.")

# /removesudo Command (Owner Only)
async def removesudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_USER_ID:
        logger.warning(f"Unauthorized access attempt by {update.message.from_user.id}")
        return await update.message.reply_text("❌ You are not authorized!")
    
    try:
        user_input = context.args[0] if context.args else None
        resolved_user_id = await resolve_user(context, update, user_input)

        if not resolved_user_id:
            return await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")

        remove_sudo(resolved_user_id)
        await update.message.reply_text(f"✅ User {resolved_user_id} removed from sudo!")
    except Exception as e:
        logger.error(f"Error removing sudo user: {e}")
        await update.message.reply_text("❌ Failed to remove sudo user. Please check the input.")

# /listsudo Command (Owner Only)
async def listsudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_USER_ID:
        logger.warning(f"Unauthorized access attempt by {update.message.from_user.id}")
        return await update.message.reply_text("❌ You are not authorized!")
    
    sudo_users = list_sudo_users()
    await update.message.reply_text(f"👑 Sudo Users:\n{', '.join(map(str, sudo_users))}")

# /mute Command
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.message.from_user.id)
    if not chat_member.status in ["administrator", "creator"]:
        return await update.message.reply_text("❌ You must be a group admin to mute users!")

    try:
        user_input = context.args[0] if context.args else None
        duration = int(context.args[1]) if len(context.args) > 1 else 60  # Default to 60 minutes
        resolved_user_id = await resolve_user(context, update, user_input)

        if not resolved_user_id:
            return await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")

        # Mute the user
        permissions = ChatPermissions(can_send_messages=False)
        until_date = datetime.now() + timedelta(minutes=duration)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=resolved_user_id,
            permissions=permissions,
            until_date=until_date
        )
        add_muted_user(resolved_user_id, until_date.isoformat())
        await update.message.reply_text(f"✅ User has been muted for {duration} minutes.")
    except Exception as e:
        logger.error(f"Error while muting user: {e}")
        await update.message.reply_text("❌ Failed to mute the user. Please check the bot's permissions.")

# /unmute Command
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.message.from_user.id)
    if not chat_member.status in ["administrator", "creator"]:
        return await update.message.reply_text("❌ You must be a group admin to unmute users!")

    try:
        user_input = context.args[0] if context.args else None
        resolved_user_id = await resolve_user(context, update, user_input)

        if not resolved_user_id:
            return await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")

        # Unmute the user
        permissions = ChatPermissions(can_send_messages=True)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=resolved_user_id,
            permissions=permissions
        )
        remove_muted_user(resolved_user_id)
        await update.message.reply_text("✅ User has been unmuted.")
    except Exception as e:
        logger.error(f"Error while unmuting user: {e}")
        await update.message.reply_text("❌ Failed to unmute the user. Please check the bot's permissions.")

# /ping Command
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = datetime.now()
    message = await update.message.reply_text("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await message.edit_text(f"**Pong!** 🏓\nLatency: `{ms} ms`", parse_mode=ParseMode.MARKDOWN)

# /info Command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    info_text = (
        f"👤 **User Info**\n\n"
        f"● ID: `{user.id}`\n"
        f"● Username: @{user.username}\n"
        f"● Name: {user.first_name} {user.last_name or ''}\n"
        f"● Is Sudo: {is_sudo_user(user.id)}\n"
        f"● Is Exempt: {is_exempt_user(user.id)}"
    )
    await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)

# Resolve user by ID, username, or mention
async def resolve_user(context, update, user_input):
    try:
        if str(user_input).isdigit():
            return int(user_input)
        elif update.message.reply_to_message:
            return update.message.reply_to_message.from_user.id
        elif update.message.entities:
            for entity in update.message.entities:
                if entity.type == MessageEntity.MENTION:
                    username = update.message.text[entity.offset:entity.offset + entity.length].lstrip('@')
                    user = await context.bot.get_chat(username)
                    return user.id
        else:
            raise ValueError("Invalid user input.")
    except Exception as e:
        logger.error(f"Error resolving user: {e}")
        await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")
        return None

# Handler to delete edited messages
async def delete_edited_messages(update: Update, context):
    if update.edited_message:
        user_id = update.edited_message.from_user.id

        # Check if the user is exempt from deletion
        if is_exempt_user(user_id):
            return  # Do nothing if the user is exempt

        user_mention = update.edited_message.from_user.mention_html()

        # Delete the edited message
        await context.bot.delete_message(
            chat_id=update.edited_message.chat_id,
            message_id=update.edited_message.message_id
        )

        # Notify the group about the deleted edited message
        await context.bot.send_message(
            chat_id=update.edited_message.chat_id,
            text=f"🚫 {user_mention}, edited messages are not allowed and have been deleted!",
            parse_mode=ParseMode.HTML
        )

# Handler to delete links, PDFs, long messages, and notify the user
async def delete_invalid_messages(update: Update, context):
    user_id = update.message.from_user.id

    # Check if the user is exempt from deletion
    if is_exempt_user(user_id):
        return  # Do nothing if the user is exempt

    user_mention = update.message.from_user.mention_html()

    # Check if the message contains a link or PDF
    if (update.message.entities and any(entity.type in [MessageEntity.URL, MessageEntity.TEXT_LINK] for entity in update.message.entities)) or \
            update.message.document:
        await update.message.delete()

        # Notify the group about the deleted message
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"🚫 {user_mention}, links or PDFs are not allowed and have been deleted!",
            parse_mode=ParseMode.HTML
        )

    # Check if the message exceeds the maximum length
    elif len(update.message.text) > MAX_MESSAGE_LENGTH:
        await update.message.delete()

        # Notify the group about the deleted message
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"🚫 {user_mention}, long messages are not allowed and have been deleted!",
            parse_mode=ParseMode.HTML
        )

# Handler to track new chat members
async def track_group(update: Update, context):
    for user in update.message.new_chat_members:
        logger.info(f"New member joined: {user.id} - {user.username}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Welcome, {user.mention_html()}! 🎉",
            parse_mode=ParseMode.HTML
        )

# Handler to track left chat members
async def track_left_member(update: Update, context):
    user = update.message.left_chat_member
    logger.info(f"Member left: {user.id} - {user.username}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Goodbye, {user.mention_html()}! 👋",
        parse_mode=ParseMode.HTML
    )

# /broadcast Command (Owner Only)
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_USER_ID:
        return await update.message.reply_text("❌ You are not authorized!")

    message = " ".join(context.args)
    if not message:
        return await update.message.reply_text("Usage: /broadcast <message>")

    # Send the message to all groups
    for chat_id in GROUP_CHAT_IDS:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logger.error(f"Failed to send broadcast to {chat_id}: {e}")

    await update.message.reply_text("✅ Broadcast sent to all groups.")

# Enable nested asyncio loops (Fixes RuntimeError in Heroku, Jupyter, etc.)
nest_asyncio.apply()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a simple error handler function
async def error_handler(update, context):
    """Handles all bot errors."""
    logger.error(f"Exception: {context.error}", exc_info=True)

async def start_bot():
    """Initialize and run the bot."""
    application = Application.builder().token("7632046793:AAHhp2Ow-qknHsPPuffmPqQ5Qm7RPQJ1DcU").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("add", addsudo))
    application.add_handler(CommandHandler("remove", removesudo))
    application.add_handler(CommandHandler("listsudo", listsudo))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, delete_edited_messages))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_invalid_messages))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_group))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, track_left_member))
    application.add_handler(CommandHandler("broadcast", broadcast_message))

    # Add the missing error handler
    application.add_error_handler(error_handler)

    logger.info("Bot is running...")

    try:
        await application.run_polling()
    except Exception as e:
        logger.error(f"Error in polling: {e}", exc_info=True)
    finally:
        await application.shutdown()
        logger.info("Bot process finished.")

def main():
    """Run the bot safely."""
    loop = asyncio.get_event_loop()
    
    if loop.is_running():
        # If inside an existing event loop, create a background task
        loop.create_task(start_bot())
    else:
        # Run normally if no event loop is active
        asyncio.run(start_bot())

if __name__ == "__main__":
    main()
