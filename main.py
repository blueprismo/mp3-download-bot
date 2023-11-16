#!/usr/bin/env python3.11
import logging
# Logging
logging.basicConfig(
    format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
import youtube_downloader
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, Application, CallbackQueryHandler

# Load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
# avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

# Constants
HELP_TEXT = """
This bot is used to download mp3 files from different sources,
start with the /start command, to select the source you want to download from.
Afterwards send a link to the bot and it will return you the mp3 archive!
"""


# Commands
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function returns all the arguments from the command to upper case"""
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_caps
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    This function answers to the /start command,
    the start command will display a inline Keyboard: https://core.telegram.org/bots/features#inline-keyboards
    it should return a string with the value we want to use
    """
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Display inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("Youtube", callback_data="youtube"),
            InlineKeyboardButton("Spotify", callback_data="spotify"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    return "youtube"


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
    return "youtube"


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function displays some help"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=HELP_TEXT
    )


# Functions
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function mirrors all the messages that arrive to the bot."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


# Extract the youtube URL functions!
# https://docs.python-telegram-bot.org/en/v20.6/telegram.bot.html#telegram.Bot.send_audio
async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function gets a youtube link, then transforms it to mp3.
    The mp3 is stored in a storagebox
    Then a URL is returned serving that mp3 files
    """
    logger.info(f'Received a URL to convert:\n{update.message.text}')
    url = youtube_downloader.convert_mp3_fs(update.message.text)
    logger.info('URL Converted')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🎶Here's your mp3 url: {url}"
    )


async def youtube_stream(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function gets a youtube link, then transforms it to mp3.
    The main drawback is that in telegram the audios cannot be downloaded
    into the phone local storage 😭
    """
    music, metadata = youtube_downloader.convert_mp3_buffer(update.message.text)

    await context.bot.send_audio(
        chat_id=update.effective_chat.id,
        audio=music,
        title=metadata['Title'],
        filename=metadata['Title'],
        caption=f"Here's your youtube video in mp3 format 🎶,\nSize: {metadata['Size']:.2f} MB"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This function catches all the unknown commands"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command, please use the /start command to get started 😎\nor the /help command if you need help 🤔"
    )


# Bot commands
async def post_init(application: Application) -> None:
    """
    This post_init will be for initial configuration for the bots, like the button menu
    specified in https://docs.python-telegram-bot.org/en/v20.6/telegram.menubuttoncommands.html#telegram.MenuButtonCommands
    """
    await application.bot.set_my_commands([('start', 'Starts the bot'), ('help', 'Show some help')])
    await application.bot.set_chat_menu_button()


# Main program
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['BOT_TOKEN']).post_init(post_init).build()

    # Instantiate the handlers
    youtube_handler = MessageHandler(filters.TEXT & (filters.Entity("url") | filters.Entity("text_link")) & filters.Regex(r'.*youtube.*'), youtube)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Register the handlers
    # Message handlers
    application.add_handler(youtube_handler)
    application.add_handler(echo_handler)

    # Command handlers
    application.add_handler(CommandHandler('caps', caps))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('help', help))

    # This should be the last handler ALWAYS
    application.add_handler(unknown_handler)

    # Run the bot
    application.run_polling()
