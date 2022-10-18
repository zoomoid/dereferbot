import logging
from urllib.parse import urlparse
from bot.common_cleaner import CommonCleaner

from bot.spotify_cleaner import SpotifyCleaner
from bot.twitter_cleaner import TwitterCleaner

def root(hostname: str) -> str:
    """
    root returns the root hostname of an arbitrary domain name

    :returns: a string that is the root DNS name of an arbitrary hostname
    """
    return ".".join(hostname.split(".")[-2:])

class Selector:
    @staticmethod
    def query(input: str):
        q = urlparse(input)
        r = root(q.hostname)
        logging.info(r)
        if r in SpotifyCleaner.Hostnames:
            logging.info("starting new spotify cleaner")
            return SpotifyCleaner(q)
        elif r in TwitterCleaner.Hostnames:
            logging.info("starting new twitter cleaner")
            return TwitterCleaner(q)
        else:
            return CommonCleaner(q, [])
