import asyncio

import httpx
from settings import config
from data_storage import DataStorage
import logging


DS = DataStorage()
logger = logging.getLogger(__name__)

async def fetch_data(url: str):
    try:
        async with httpx.AsyncClient() as client:
            logger.info('Отправляю запрос')
            response = await client.get(url)
            logger.info('Притянул данные')
    except asyncio.CancelledError:
        logger.info('Задача отменена')
    except:
        logger.info('Падение запроса!')
    else:
        asyncio.create_task(DS.add_data(response.text))
        logger.info('Создал задачу добавления в хранилище')

        

class Parser:
    async def run_parser(self):
        while True:
            tasks: list[asyncio.Task] = [asyncio.create_task(fetch_data(config.url)) for _ in range(3)]
            logger.info('Создал дублирующие задачи')
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in pending:
                task.cancel()
                logger.info('Отменил дублирующую задачу')
            await asyncio.sleep(1)      


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    parser = Parser()
    asyncio.run(parser.run_parser())
