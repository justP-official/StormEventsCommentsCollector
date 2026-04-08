from typing import Any

import httpx

from comments.exceptions import ClientError


class Client:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            timeout: int = 10
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Content-Type": "application/x-www-form-encoded",
                "Authorization": f"Bearer {api_key}"
            },
            timeout=timeout,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def _request(
            self,
            method: str,
            url: str,
            params: dict = None,
            data: dict = None,
            **kwargs: Any
    ) -> httpx.Response:
        """
        Общий метод для выполнения запросов.

        :param method: HTTP метод
        :param url: Endpoint, на который отправится запрос
        :param kwargs: Параметры запроса
        :return: Объект ответа
        """
        try:
            response = await self._client.request(method, url, params=params, data=data)
            response.raise_for_status()
            return response
        except httpx.TimeoutException as e:
            raise ClientError("API не отвечает") from e
        except httpx.HTTPStatusError as e:
            raise ClientError(f"HTTP {e.response.status_code}") from e
        except httpx.HTTPError as e:
            raise ClientError("Ошибка сети") from e

    async def get(self, url: str, params = None, data = None, **kwargs: Any) -> httpx.Response:
        return await self._request("GET", url, params=params, data=data, **kwargs)

    async def post(self, url: str, params = None, data = None, **kwargs: Any) -> httpx.Response:
        return await self._request("POST", url, data=data, params=params, **kwargs)
