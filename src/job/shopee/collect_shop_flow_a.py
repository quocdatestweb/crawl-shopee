import os
import sys
import json
import logging
import asyncio
import aiohttp
import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(utils_dir)

from utils.utils import timer
from repository.shop_repository import ShopRepository
from config.database import Session
from config.config import settings
from config.database import check_database_connection
from config.proxy import proxy

# Initialize the session
session = Session()

# Setup path to log file
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(f"/crawler/log/{current_time}collect_shop_flow_a.log")

# Initialize logger
logger = logging.getLogger(__name__)


class CollectShopsA:
    def __init__(self):
        check_database_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.base_url = (
            "https://shopee.co.th/api/v4/official_shop/get_shops_by_category/?"
        )
        self.shop_repository = ShopRepository(session)

    @timer
    def __call__(self, categories):
        for category in categories:
            crawler_urls = []
            crawler_urls.append(f"{self.base_url}&category_id={category}")
            asyncio.run(self.main(crawler_urls))
            logger.info(f"└── Add shop mall of category {category}")

        session.close()
        exit()

    async def main(self, crawlerUrls):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "referer": "https://shopee.co.th/",
            "X-Requested-With": "XMLHttpRequest",
        }
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=10),
            headers=headers,
        ) as client:
            tasks = [self.task(client, query_url) for query_url in crawlerUrls]
            await asyncio.gather(*tasks)

    async def task(self, client, query_url):
        raw_data = await self.fetch_from_shopee(client, query_url)
        list_shops = await self.parse_data(raw_data)

        if list_shops is not None:
            self.save_shop(list_shops)

    async def fetch_from_shopee(self, client, query_url):
        try:
            async with client.get(query_url) as response:
                raw_data = await response.text()
                assert response.status == 200
                return raw_data
        except Exception as e:
            logger.warning(
                f"Exception: {query_url} - Fetch shop mall from shopee failed"
            )
            return None

    async def parse_data(self, raw_data):
        if raw_data is None:
            return None
        info = json.loads(raw_data)
        list_shops = []
        for item in info["data"]["brands"]:
            for sub_item in item["brand_ids"]:
                item_info = self.shop_repository.model(
                    shop_id=sub_item["shopid"],
                    username=sub_item["username"],
                )
                list_shops.append(item_info)
        return list_shops

    def save_shop(self, list_shops):
        try:
            for shop in list_shops:
                is_shop_existed = bool(self.shop_repository.get_shop_by_shop_id(shop))
                if is_shop_existed:
                    logger.info(f"├── Shop {shop.username} is existed")
                    continue
                logger.info(f"├── Added shop {shop.username} ...")
                self.shop_repository.create(shop)

        except Exception as e:
            logger.warning(f"Exception: save shop mall failed")
            session.rollback()


if __name__ == "__main__":
    logger.info(f"├── Start collect shop mall")
    categories = ["11044959"]
    collect_shops = CollectShopsA()
    collect_shops(categories)
