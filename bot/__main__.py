import logging
import os

from telegram import Update
from telegram.ext import CommandHandler, Application, InlineQueryHandler

from . import handlers

TOKEN = os.environ.get("DEREFER_BOT_TOKEN")
NAME = os.environ.get("DEREFER_BOT_NAME", "derefbot")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(InlineQueryHandler(handlers.reply_to_inline))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
