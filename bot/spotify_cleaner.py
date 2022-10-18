from urllib.parse import ParseResult
from bot.common_cleaner import CommonCleaner

class SpotifyCleaner(CommonCleaner):

    Hostnames: list[str] = ["spotify.com", "open.spotify.com"]

    Specific: list[str] = ["si", "context", "pt"]

    def __init__(self, url: ParseResult) -> None:
        super().__init__(url, self.Specific)

    # def results():
    #     return super().results()
