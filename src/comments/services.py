import asyncio

from comments.client import Client
from comments.exceptions import ClientError
from comments.helpers import CommentsHelper


class CommentsService:
    def __init__(
            self,
            base_url: str,
            api_key: str,
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key

    async def fetch_comments(self, topic_url, client: Client) -> list:
        print("Собираем комментарии...")

        group_id, topic_id = await CommentsHelper.parse_url(topic_url)

        comments = []
        offset = 1  # Пропускаем первый комментарий от группы
        count_per_request = 100

        while True:
            response = await client.get(
                "board.getComments",
                params={
                    "group_id": group_id,
                    "topic_id": topic_id,
                    "offset": offset,
                    "count": count_per_request,
                    "v": "5.199",
                },
            )
            data = response.json()

            if data.get("error"):
                raise ClientError(data.get("error").get("error_msg"))

            items = data.get("response").get("items")

            if not items:
                break

            comments += items
            offset += count_per_request

            await asyncio.sleep(3)

        return comments

    async def get_users_links(self, comments: list, client: Client) -> list:
        print("Получаем ссылки пользователей...")

        users_links = []

        for comment in comments:
            users_links.append("https://vk.com/id" + str(comment.get("from_id")))

        return users_links

    async def run(self, topic_url):
        async with Client(
            self._base_url,
            self._api_key,
        ) as client:
            comments = await self.fetch_comments(topic_url, client)

            users_links = await self.get_users_links(comments, client)

            return await CommentsHelper.to_dict(comments, users_links)
