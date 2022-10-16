import logging
import os

from telegram.ext import CommandHandler, Updater
from telegram.ext.inlinequeryhandler import InlineQueryHandler

from . import handlers

token = os.environ.get("DEREFER_BOT_TOKEN")
bot_name = os.environ.get("DEREFER_BOT_NAME", "derefbot")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main() -> None:
    bot = Updater(token=token, use_context=True)
    dispatcher = bot.dispatcher

    help_handler = CommandHandler("help", handlers.help_command)
    inline_handler = InlineQueryHandler(handlers.reply_to_inline)

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(inline_handler)

    bot.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM, or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    bot.idle()


if __name__ == "__main__":
    main()
