import hashlib
import logging
from typing import Callable

from urllib.parse import ParseResult, parse_qsl, urlencode, urlparse, urlunparse

from telegram import InlineQueryResultArticle, InputTextMessageContent


HookResult = str
HookIdentifier = tuple[str, str]
HookReturn = tuple[HookResult, HookIdentifier]

Hook = Callable[[ParseResult], HookReturn]


class CommonCleaner:

    Common: list[str] = [
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "utm_content",
        "utm_term",
    ]

    Specific: list[str] = []

    Hostnames: list[str] = []

    __url: str = ""
    __no_action: bool = False

    __parsed: ParseResult = None
    __cleaned: ParseResult = None

    __output: str = ""

    __hooks: list[Hook] = []

    def __init__(self, url: ParseResult, specific: list[str]) -> None:
        self.__parsed = url
        self.Specific += specific

        if self.__parsed.hostname == None:
            self.__no_action = True

        self.clean_url()

    def clean_url(
        self,
    ):
        if self.__no_action:
            return self

        qs_to_remove = self.Common + self.Specific
        qsl = parse_qsl(self.__parsed.query)

        new_qs = [(key, value) for (key, value) in qsl if key not in qs_to_remove]
        new_qs = urlencode(new_qs)
        self.__cleaned = self.__parsed._replace(query=new_qs)
        self.__output = urlunparse(self.__cleaned)
        return self

    def output(self) -> str:
        return self.__output

    def root(self) -> str:
        if self.__parsed == None:
            return ""
        return ".".join(self.__parsed.hostname.split(".")[-2:])

    def register(self, hook: Hook):
        self.__hooks += [hook]
        return self

    def results(self) -> list[InlineQueryResultArticle]:
        base = [
            InlineQueryResultArticle(
                id=hashlib.sha256(f"{self.__url}".encode("utf-8")).hexdigest(),
                title="Deref'd URL",
                description=self.__output,
                input_message_content=InputTextMessageContent(
                    message_text=self.__output
                ),
            )
        ]
        hook_results = [h(self.__cleaned) for h in self.__hooks]
        res = base + [
            InlineQueryResultArticle(
                id=hashlib.sha256(f"{s}-{title}-{desc}".encode("utf-8")).hexdigest(),
                title=title,
                description=desc,
                input_message_content=InputTextMessageContent(message_text=s),
            )
            for (s, (title, desc)) in hook_results
        ]
        return res
