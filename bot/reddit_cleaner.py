from urllib.parse import ParseResult, urlunparse
from bot.common_cleaner import CommonCleaner, HookReturn
import requests

from . import __version__

def hook_short_reddit_link(query: ParseResult) -> HookReturn:
    source_url = urlunparse(query)
    r = requests.get(source_url + ".json", headers={"user-agent": f"web:dereferbot:{__version__} (by /u/deleted)"})

    short_url = r.json()[0]["data"]["children"][0]["data"]["url_overridden_by_dest"] or source_url
    return short_url, ("reddit.com -> i.redd.it", "Gets the direct link to an image to embed")

class RedditCleaner(CommonCleaner):
    Hostnames: list[str] = ["reddit.com", "old.reddit.com"]

    Specific: list[str] = []

    def __init__(self, url: ParseResult) -> None:
        super().__init__(url, self.Specific)
        self.register(hook_short_reddit_link)
