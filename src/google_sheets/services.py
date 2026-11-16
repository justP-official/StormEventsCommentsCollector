import asyncio

import gspread
from gspread.utils import rowcol_to_a1

from dotenv import find_dotenv, load_dotenv

from common.decorators import measure_time

load_dotenv(find_dotenv(".env"))

class GoogleSheetsService:
    __EXCLUDED_WORKSHEETS = {
        "Список",
        "Общий",
        "Наши тексты",
        "Штрафы",
    }

    def __init__(
            self,
            credentials_file_path: str,
            sheet_url: str
    ):
        self._client = gspread.service_account(filename=credentials_file_path)
        self._sheet = self._client.open_by_url(sheet_url)

    async def get_worksheets(self) -> list[gspread.Worksheet]:
        print("Получаем листы...")
        return [sheet for sheet in self._sheet.worksheets() if sheet.title not in self.__EXCLUDED_WORKSHEETS]

    async def get_authors(self, worksheet: gspread.Worksheet):
        print(f"Собираем запускантов с листа: {worksheet.title}")
        # убираем пустые строки и заголовок с подвалом

        column = worksheet.col_values(1)[2:] # берём первую колонку и отсекаем заголовок

        authors = []

        for author in column:
            if not author:
                break
            authors.append(author)

        return authors

    @measure_time
    async def insert_data(self, data: dict, day: int = 1):
        START_COL = 4
        COL_OFFSET = 5
        col = START_COL + COL_OFFSET * (day - 1)

        worksheets = await self.get_worksheets()

        counters = dict.fromkeys((s.title for s in worksheets), 0)

        for worksheet in worksheets:
            users = await self.get_authors(worksheet)

            if users:
                links = []
                for user in users:
                    text = data.get(user, '---')

                    if text != '---':
                        counters[worksheet.title] += 1

                    links.append([text])

                start_cell = rowcol_to_a1(
                    worksheet.find(users[0]).row,
                    col
                )
                end_cell = rowcol_to_a1(
                    worksheet.find(users[-1]).row,
                    col
                )

                print(f"Обновляем диапазон {start_cell}:{end_cell}")

                worksheet.batch_update([
                    {
                        "range": f"{start_cell}:{end_cell}",
                        "values": links
                    }
                ])
            await asyncio.sleep(1)

        print(f"Собрано текстов по заданию №{day}:")

        for reader, counts in counters.items():
            print(reader, counts, end='\n')
