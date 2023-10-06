import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.selector import Selector

help_message = """
Dereferbot removes obnoxious and nasty tracking and ref links from URLs.

Created mostly out of spite because Spotify's Share links get longer and
longer each day, as they add more and more tracking data.

Can also shorten reddit links to their image CDN origin, and replace twitter/x
urls with a proxy that properly serves post metadata (fxtwitter.com).

Created by @zoomoid on [https://github.com/zoomoid/dereferbot](https://github.com/zoomoid/dereferbot).
"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to private messages requesting help
    """
    await update.message.reply_markdown_v2(help_message)


async def reply_to_inline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        await update.inline_query.answer(results)
    except Exception as e:
        logging.error(e)
        return
