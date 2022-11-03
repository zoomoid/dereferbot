import logging

from telegram import (
    ParseMode,
    Update,
)
from telegram.ext import CallbackContext

from bot.selector import Selector

help_message = """
Dereferbot removes obnoxious and nasty tracking and ref links from URLs.

Created mostly out of spite because Spotify's Share links get longer and
longer each day, as they add more and more tracking data.

Created by @zoomoid on [https://github.com/zoomoid/dereferbot](https://github.com/zoomoid/dereferbot).
"""


def help_command(update: Update, context: CallbackContext):
    """
    Responds to private messages requesting help
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
        results = Selector.query(query).results()
        context.bot.answer_inline_query(update.inline_query.id, results)
        return
    except Exception as e:
        logging.error(e)
        return
