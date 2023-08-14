from urllib.parse import ParseResult, urlunparse
from bot.common_cleaner import CommonCleaner, HookReturn

def hook_fxtwitter(query: ParseResult) -> HookReturn:
    n = query._replace(netloc="fxtwitter.com")
    return urlunparse(n), ("twitter -> fxtwitter", "Twitter, but metadata tags are fixed")


class TwitterCleaner(CommonCleaner):
    Hostnames: list[str] = ["twitter.com", "t.co", "x.com"]

    Specific: list[str] = ["s", "t"]

    def __init__(self, url: ParseResult) -> None:
        super().__init__(url, self.Specific)
        self.register(hook_fxtwitter)
