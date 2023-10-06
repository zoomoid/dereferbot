from urllib.parse import urlparse
from bot.common_cleaner import CommonCleaner

from bot.spotify_cleaner import SpotifyCleaner, SpotifyLinkCleaner
from bot.twitter_cleaner import TwitterCleaner

def root(hostname: str) -> str:
    """
    root returns the root hostname of an arbitrary domain name

    :return: a string that is the root DNS name of an arbitrary hostname.
    """
    return ".".join(hostname.split(".")[-2:])

class Selector:
    @staticmethod
    def query(input: str):
        q = urlparse(input)
        r = root(q.hostname)
        if r in SpotifyCleaner.Hostnames:
            return SpotifyCleaner(q)
        elif r in TwitterCleaner.Hostnames:
            return TwitterCleaner(q)
        elif r in SpotifyLinkCleaner.Hostnames:
            return SpotifyLinkCleaner(q)
        else:
            return CommonCleaner(q, [])
