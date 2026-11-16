import re

from comments.exceptions import HalperException


class CommentsHelper:
    __URL_PATTERN = re.compile(
    r'(?i)\b(?:https?://)?(?:www\.)?'
    r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+'
    r'[a-z]{2,}'
    r'(?::\d{1,5})?(?:/[^\s<>"\')\]]*)?'
    )
    __VK_TOPIC_PATTERN = r'^https://vk\.ru/topic-\d+_\d+$'

    @classmethod
    async def get_url(cls) -> str | None:
        while True:
            url = input("Введите ссылку на обсуждение (или 0 для выхода): ")
            if url == "0":
                raise HalperException("Выход")
            if re.match(cls.__VK_TOPIC_PATTERN, url):
                return url
            continue


    @classmethod
    async def parse_url(cls, url: str) -> tuple:
        return tuple(url.split("-")[-1].split("_"))

    @staticmethod
    async def get_day() -> int | None:
        while True:
            try:
                day = int(input("Введите день запуска (от 1 до 12 или 0 для выхода): "))
                if day == 0:
                    raise HalperException("Выход")
                if not 1 <= day <= 12:
                    continue
                return day
            except ValueError:
                continue

    @classmethod
    async def clean_url(cls, url: str) -> str | None:
        match = cls.__URL_PATTERN.search(url)
        return match.group(0) if match else None

    @classmethod
    async def to_dict(cls, comments: list, users_links: list) -> dict[str, str]:
        d = {}

        for link, comment in zip(users_links, comments):
            cleaned_comment = await cls.clean_url(comment.get("text"))

            if link in d:
                continue

            if cleaned_comment is None:
                continue

            d[link] = cleaned_comment

        return d
