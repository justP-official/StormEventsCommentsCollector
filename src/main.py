import asyncio
import os

from dotenv import find_dotenv, load_dotenv

from comments.services import CommentsService
from google_sheets.services import GoogleSheetsService
from comments.exceptions import ClientError, HalperException
from comments.helpers import CommentsHelper

load_dotenv(find_dotenv(".env"))


async def main():
    try:
        comments_service = CommentsService(
            "https://api.vk.ru/method/",
            os.environ.get("VK_TOKEN")
        )

        board_link = await CommentsHelper.get_url()

        day = await CommentsHelper.get_day()

        comments = await comments_service.run(board_link)

        google_sheet_service = GoogleSheetsService(
            "src/google_sheets/creds.json",
            os.environ.get("GOOGLE_SHEET_URL")
        )

        await google_sheet_service.insert_data(comments, day=day)
    except (ClientError, HalperException) as e:
        print(e)
    else:
        print("Готово!")


if __name__ == "__main__":
    asyncio.run(main())
