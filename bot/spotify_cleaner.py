from urllib.parse import ParseResult, urlunparse, urlparse, parse_qsl, urlencode
from bot.common_cleaner import CommonCleaner, HookReturn
import requests

def hook_spotify_link(query: ParseResult) -> HookReturn:
    # https://spotify.link/L1Sb5i2ruDb -> HTTP 307 with Location header set to the "original" open.spotify.com URL
    url = urlunparse(query)
    res = requests.get(url, allow_redirects=False)

    new_loc = res.headers.get("Location", url)
    new_url = urlparse(new_loc)
    new_qsl = parse_qsl(new_url.query)

    qs_to_remove = [
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_content",
        "utm_term",
        "pt",
        "_branch_match_id",
        "nd"
        # exclude ?si, because we just want to reset that in order to preserve client navigation functionality
        # afaik, this parameter causes the opening browser to forward the navigation to the app, both on mobile
        # and desktop. It does not matter if there's any value in si, as the empty string will also work
    ]
    new_qsl = [(key, value) for (key, value) in new_qsl if key not in qs_to_remove]
    new_qsl = [(key, value) if key != "si" else ("si", "") for (key, value) in new_qsl]

    new_url = new_url._replace(query=urlencode(new_qsl))
    return urlunparse(new_url), ("spotify.link", "remove tracking from redirect")

class SpotifyCleaner(CommonCleaner):
    Hostnames: list[str] = ["spotify.com", "open.spotify.com"]

    Specific: list[str] = ["si", "context", "pt"]

    def __init__(self, url: ParseResult) -> None:
        super().__init__(url, self.Specific)


class SpotifyLinkCleaner(CommonCleaner):
    Hostnames: list[str] = ["spotify.link"]

    def __init__(self, url: ParseResult) -> None:
        super().__init__(url, self.Specific)
        self.register(hook_spotify_link)

