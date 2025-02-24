import os
import random
import asyncio
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ChatPermissions, User
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime, timedelta
from broadcast import broadcast_message
from config import BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = BOT_TOKEN

EXEMPT_USER_IDS = [6545754981, 7875192045, 6656608288]  
GROUP_CHAT_IDS = []

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

OWNER_USER_ID = 7379318591

GROUP_CHAT_IDS = set()

# Set a maximum length for messages
MAX_MESSAGE_LENGTH = 200

# List of video file URLs to send randomly
VIDEO_LIST = [
    "https://telegra.ph/file/1722b8e21ef54ef4fbc23.mp4",
    "https://telegra.ph/file/ac7186fffc5ac5f764fc1.mp4",
    "https://telegra.ph/file/4156557a73657501918c4.mp4",
    "https://telegra.ph/file/0d896710f1f1c02ad2549.mp4",
    "https://telegra.ph/file/03ac4a6e94b5b4401fa5a.mp4",
]


async def track_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        GROUP_CHAT_IDS.add(chat.id)
        logging.info(f"Added group {chat.title} ({chat.id}) to broadcast list.")

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
def is_exempt_user(user_id):
    return user_id in EXEMPT_USER_IDS

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
            "● If you need any kind of helo dm @xotikop_bot🩵\n"
            "● If you want to add your self in sudo,contact @xazoc.💛\n\n"
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


# Function to resolve user input
async def resolve_user(context, update, user_input):
    try:
        if str(user_input).isdigit():
            return int(user_input)
        elif update.message.reply_to_message:
            return update.message.reply_to_message.from_user.id
        elif update.message.entities:
            for entity in update.message.entities:
                if entity.type == MessageEntity.MENTION and entity.user:
                    return entity.user.id
        else:
            raise ValueError("Invalid user input.")
    except Exception as e:
        print(f"Error resolving user: {e}")
        await update.message.reply_text("❌ Could not resolve the user. Ensure input is valid.")
        return None



import requests

def get_user_id_from_username(bot, username):
    url = f"https://api.telegram.org/bot{TOKEN}/getChatMember"
    params = {"chat_id": username, "user_id": username}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        chat_member = response.json()["result"]
        return chat_member["user"]["id"]
    else:
        return None

#user_id = get_user_id_from_username(Application, username)

# Command to add a user to sudo
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Adds a user to the sudo list. Accepts user ID, username, or mention.
    Only the owner can add users.
    """
    if update.message.from_user.id != OWNER_USER_ID:
        await update.message.reply_text("❌ You don't have permission to add sudo users!")
        return

    # Check if the command includes arguments or is a reply
    user_input = None
    if len(context.args) == 1:
        user_input = context.args[0]  # Get the username/user_id from the arguments
    elif update.message.reply_to_message:
        user_input = update.message.reply_to_message.from_user.id  # Get the user ID from the replied message

    if not user_input:
        await update.message.reply_text(
            "❌ Usage: /add <username>, <user_id>, or reply to a user's message with /add."
        )
        return

    # Resolve the user ID
    resolved_user_id = await resolve_user(context, update, user_input)

    if resolved_user_id is None:
        await update.message.reply_text("❌ Unable to resolve the user. Please ensure the input is correct.")
        return

    # Add the user to the sudo list if not already present
    if resolved_user_id not in EXEMPT_USER_IDS:
        EXEMPT_USER_IDS.append(resolved_user_id)
        await update.message.reply_text(f"✅ User {resolved_user_id} has been added to the sudo list!")
    else:
        await update.message.reply_text("❌ This user is already in the sudo list.")


async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Removes a user from the sudo list. Accepts user ID, username, or mention.
    Only the owner can remove users.
    """
    if update.message.from_user.id != OWNER_USER_ID:
        await update.message.reply_text("❌ You don't have permission to remove sudo users!")
        return

    # Check if the command includes arguments or is a reply
    user_input = None
    if len(context.args) == 1:
        user_input = context.args[0]  # Get the username/user_id from the arguments
    elif update.message.reply_to_message:
        user_input = update.message.reply_to_message.from_user.id  # Get the user ID from the replied message

    if not user_input:
        await update.message.reply_text(
            "❌ Usage: /remove <username>, <user_id>, or reply to a user's message with /remove."
        )
        return

    # Resolve the user ID
    resolved_user_id = await resolve_user(context, update, user_input)

    if resolved_user_id is None:
        await update.message.reply_text("❌ Unable to resolve the user. Please ensure the input is correct.")
        return

    # Remove the user from the sudo list if present
    if resolved_user_id in EXEMPT_USER_IDS:
        EXEMPT_USER_IDS.remove(resolved_user_id)
        await update.message.reply_text(f"✅ User {resolved_user_id} has been removed from the sudo list!")
    else:
        await update.message.reply_text("❌ This user is not in the sudo list.")







# Command to mute a user
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mutes a user in the chat. Accepts user ID, username, or mention.
    Usage: /mute <user_id|username|mention> <duration_in_minutes>
    """
    # Check if the user executing the command is an admin
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.message.from_user.id)
    if not chat_member.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You must be a group admin to mute users!")
        return

    # Check if the target user is provided or replied to
    user_input = None
    if context.args:
        user_input = context.args[0]  # Get the user identifier from arguments
    elif update.message.reply_to_message:
        user_input = update.message.reply_to_message.from_user.id

    if not user_input:
        await update.message.reply_text(
            "❌ Usage: /mute <user_id|username|mention> <duration_in_minutes>, or reply to a user's message."
        )
        return

    # Parse the mute duration
    try:
        duration = int(context.args[1]) if len(context.args) > 1 else 60  # Default to 60 minutes
        if duration <= 0:
            raise ValueError("Duration must be a positive integer.")
    except (ValueError, IndexError):
        await update.message.reply_text("❌ Invalid duration. Please provide a positive number of minutes.")
        return

    # Resolve the target user
    resolved_user_id = await resolve_user(context, update, user_input)

    if not resolved_user_id:
        await update.message.reply_text(
            f"❌ Could not resolve the user '{user_input}'. Please provide a valid input or reply to a user."
        )
        return

    # Check if the target user is an admin
    target_chat_member = await context.bot.get_chat_member(update.effective_chat.id, resolved_user_id)
    if target_chat_member.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You cannot mute another admin!")
        return

    # Mute the target user
    try:
        permissions = ChatPermissions(can_send_messages=False)
        until_date = datetime.now() + timedelta(minutes=duration)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=resolved_user_id,
            permissions=permissions,
            until_date=until_date
        )
        await update.message.reply_text(f"✅ User has been muted for {duration} minutes.")
    except Exception as e:
        print(f"Error while muting user: {e}")
        await update.message.reply_text("❌ Failed to mute the user. Please check the bot's permissions.")




# Command to unmute a user
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Unmutes a user in the chat. Accepts user ID, username, or mention.
    Usage: /unmute <user_id|username|mention>, or reply to a user's message.
    """
    # Check if the user executing the command is an admin
    chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.message.from_user.id)
    if not chat_member.status in ["administrator", "creator"]:
        await update.message.reply_text("❌ You must be a group admin to unmute users!")
        return

    # Check if the target user is provided or replied to
    user_input = None
    if context.args:
        user_input = context.args[0]  # Get the user identifier from arguments
    elif update.message.reply_to_message:
        user_input = update.message.reply_to_message.from_user.id

    if not user_input:
        await update.message.reply_text(
            "❌ Usage: /unmute <user_id|username|mention>, or reply to a user's message."
        )
        return

    # Resolve the target user
    resolved_user_id = await resolve_user(context, update, user_input)

    if not resolved_user_id:
        await update.message.reply_text(
            f"❌ Could not resolve the user '{user_input}'. Please provide a valid input or reply to a user."
        )
        return

    # Unmute the target user
    try:
        permissions = ChatPermissions(can_send_messages=True)  # Allow the user to send messages
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=resolved_user_id,
            permissions=permissions
        )
        await update.message.reply_text("✅ User has been unmuted.")
    except Exception as e:
        print(f"Error while unmuting user: {e}")
        await update.message.reply_text("❌ Failed to unmute the user. Please check the bot's permissions.")












# /ping Command
async def ping_u(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = datetime.now()
    event = await update.message.reply_text("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit_text(f"**I'm On**\n\n__Pong__ !! {ms} ms", parse_mode=ParseMode.MARKDOWN)

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

# Error handler function
async def error_handler(update: Update, context):
    print(f"Error: {context.error}")


# Handler to add user ID to the EXEMPT_USER_IDS list
async def add_user_command(update: Update, context):
    # Only allow the owner to use this command
    if update.message.from_user.id != OWNER_USER_ID:
        await update.message.reply_text("❌ You don't have permission to add users!")
        return


async def start_bot():
    """Initialize and run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("add", add_user))
    application.add_handler(CommandHandler("remove", remove_user))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("unmute", unmute_user))
    application.add_handler(CommandHandler("ping", ping_u))
    application.add_handler(CommandHandler("info", get_user_id_from_username))
    application.add_handler(MessageHandler(filters.UpdateType.EDITED_MESSAGE, delete_edited_messages))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_invalid_messages))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, track_group))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, track_group))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_error_handler(error_handler)

    logger.info("Bot is running...")
    try:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        await asyncio.Event().wait()  # Keeps the bot running
    except Exception as e:
        logger.error(f"Critical Error in start_bot: {e}")
    finally:
        await application.shutdown()
        await application.stop()

def main():
    """Run the bot safely."""
    try:
        logger.info("Starting bot...")
        asyncio.run(start_bot())
    except RuntimeError as e:
        logger.error(f"Critical Error in main: {e}")
    finally:
        logger.info("Bot process finished.")

if __name__ == "__main__":
    main()
