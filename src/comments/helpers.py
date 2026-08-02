import re

from comments.exceptions import HalperException


class CommentsHelper:
    __URL_PATTERN = r'^(?:https?://)?(?:www\.)?[^\s<>"\')\]]+'
    __VK_TOPIC_PATTERN = r'^https://vk\.com/topic-\d+_\d+$'

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
    async def clean_url(cls, url: str) -> str:
        try:
            return re.findall(cls.__URL_PATTERN, url)[0]
        except IndexError:
            return "None"

    @classmethod
    async def to_dict(cls, comments: list, users_links: list) -> dict[str, str]:
        return {link: await cls.clean_url(comment.get("text")) for link, comment in zip(users_links, comments)}
