import hashlib
import logging
import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from telegram import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    Update,
    ParseMode,
)
from telegram.ext import CallbackContext, CommandHandler, Updater
from telegram.ext.inlinequeryhandler import InlineQueryHandler

token = os.environ.get("DEREFER_BOT_TOKEN")
bot_name = os.environ.get("DEREFER_BOT_NAME", "derefbot")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

KNOWN_QUERY_KEYS = [
    "si",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
]


def help_command(update: Update, context: CallbackContext):
    """
    Responds to private messages requesting help
    """
    help_message = """
    Dereferbot removes obnoxious and nasty tracking and ref links from URLs.

    Created mostly out of spite because Spotify's Share links get longer and
    longer each day, as they add more and more tracking data.

    Created by @zoomoid on [https://github.com/zoomoid/dereferbot](https://github.com/zoomoid/dereferbot).
  """
    update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)


def reply_to_inline(update: Update, context: CallbackContext):
    """
    Tries to parse a query to an url and removes all known query string keys and their values from the URL,
    then responds to the query with a singleton article that contains the cleaned URL as return.
    If the url is not parsable, a singleton article is returned that informs the user that their
    URL failed to be parsed
    """
    query = update.inline_query.query
    if not query:
        return

    try:
        url = urlparse(query)
        qsl = parse_qsl(url.query)
        new_qs = [(key, value) for (key, value) in qsl if key not in KNOWN_QUERY_KEYS]
        new_qs = urlencode(new_qs)
        new_url = url._replace(query=new_qs)
        new_url = urlunparse(new_url)
        results = [
            InlineQueryResultArticle(
                id=hashlib.sha256(f"{query}".encode("utf-8")).hexdigest(),
                title="Deref'd URL",
                description=new_url,
                input_message_content=InputTextMessageContent(message_text=new_url),
            )
        ]
        context.bot.answer_inline_query(update.inline_query.id, results)
        return
    except:
        # query is not a parsable URL
        # results = [
        #   InlineQueryResultArticle(
        #     id=hashlib.sha256(f"{query}".encode("utf-8")).hexdigest(),
        #     title="Query is not a parsable URL",
        #     description="Query is not a parsable URL"
        #   )
        # ]
        # context.bot.answer_inline_query(update.inline_query.id, results)
        return


def main() -> None:
    bot = Updater(token=token, use_context=True)
    dispatcher = bot.dispatcher

    help_handler = CommandHandler("help", help_command)
    inline_handler = InlineQueryHandler(reply_to_inline)

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(inline_handler)

    bot.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM, or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    bot.idle()


if __name__ == "__main__":
    main()
