import os
import sys
import random
import json
import logging
import asyncio
import datetime
import aiohttp

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.append(utils_dir)

from config.config import settings
from repository.shop_repository import ShopRepository
from repository.cookie_repository import CookieRepository
from repository.category_repository import CategoryRepository
from utils.utils import timer
from config.database import Session
from config.database import check_database_connection
from config.timescale import check_timescale_connection
from config.proxy import proxy

# Initialize the session
session = Session()

# Setup path to log file
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(f"/crawler/log/{current_time}-collect_shop_flow_b.log")

# Initialize logger
logger = logging.getLogger(__name__)


class CollectShopsB:
    def __init__(self):
        check_database_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.search_item_api = "https://shopee.co.th/api/v4/recommend/recommend?bundle=category_landing_page"
        today = datetime.datetime.now()
        self.today_date = today.strftime("%Y-%m-%d %H:%M:%S")
        self.category_repository = CategoryRepository(session)
        self.shop_repository = ShopRepository(session)
        self.count = 500

    @timer
    def __call__(self):
        list_categories = self.category_repository.list_all()

        self.list_category_ids = []

        for category in list_categories:
            if category.global_id is not None and category.global_id != "":
                self.list_category_ids.append(category.global_id)
            if category.local_id is not None and category.local_id != "":
                self.list_category_ids.append(category.local_id)

        for category_id in self.list_category_ids:
            crawler_urls = []

            logger.info(f"Start collect shop by category: {category_id}")
            if category_id is None or category_id == "":
                continue
            num = 0
            while num < self.count:
                crawler_urls.append(
                    f"{self.search_item_api}&catid={category_id}&limit=60&offset={num}"
                )
                num += 60
            asyncio.run(self.main(crawler_urls))
            logger.info(f"Finish collect shop by category: {category_id}")

        session.close()

    async def main(self, crawler_urls):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "referer": "https://shopee.co.th/",
            "X-Requested-With": "XMLHttpRequest",
        }
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=10),
            headers=headers,
        ) as client:
            for query_url in crawler_urls:
                await self.task(client, query_url)
                await asyncio.sleep(1)

    async def task(self, client, query_url):
        raw_data = await self.fetch_from_shopee(client, query_url)
        list_shop = await self.parse_data(raw_data)
        if list_shop is None:
            return None
        self.save_list_shop(list_shop)

    async def fetch_from_shopee(self, client, query_url):
        try:
            async with client.get(query_url, timeout=20, proxy=proxy) as response:
                raw_data = await response.text()
                assert response.status == 200
                return raw_data
        except:
            logger.warning(
                f"Exception: {query_url} Fetch shop detail from shopee failed"
            )
            return None

    async def parse_data(self, raw_data):
        try:
            if not raw_data:
                return None
            info = json.loads(raw_data)
            list_shops = []
            for item in info["data"]["sections"][0]["data"]["item"]:
                shop = self.shop_repository.model(
                    shop_id=item["shopid"],
                )
                if str(item["catid"]) in self.list_category_ids:
                    list_shops.append(shop)
            return list_shops
        except Exception as e:
            logger.warning(f"Exception: {e}")
            return None

    def save_list_shop(self, list_shops):
        try:
            for shop in list_shops:
                is_shop_existed = bool(self.shop_repository.get_shop_by_shop_id(shop))
                if is_shop_existed:
                    logger.info(f"Shop {shop.shop_id} is existed")
                    continue
                self.shop_repository.create(shop)
                logger.info(f"Create shop {shop.shop_id} successfully")

        except Exception as e:
            logger.warning(f"Exception: {e}")
            session.rollback()


if __name__ == "__main__":
    logger.info(f"Collecting shop flow B ...")
    CollectShopsB()()
