import os
import sys
import aiohttp
import random
import logging
import json
import asyncio
import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(utils_dir)

from config.config import settings
from utils.utils import timer
from repository.shop_repository import ShopRepository
from repository.cookie_repository import CookieRepository
from config.proxy import proxy
from config.database import Session
from config.database import check_database_connection

# Initialize the session
session = Session()

# Setup path to log file
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(f"/crawler/log/{current_time}-shoptracker-get_shop_detail.log")

# Initialize logger
logger = logging.getLogger(__name__)


class GetShopDetail:
    def __init__(self):
        check_database_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.base_url = "https://shopee.co.th/api/v4/shop/get_shop_base?entry_point=ShopByPDP&need_cancel_rate=true&request_source=shop_home_page&version=1&shopid="
        self.shop_repository = ShopRepository(session)

        today = datetime.datetime.now()
        self.today_date = today.strftime("%Y-%m-%d %H:%M:%S")

    @timer
    def __call__(self):
        crawler_urls = []
        list_shop = self.shop_repository.get_shop_tracker()
        for shop in list_shop:
            crawler_urls.append(f"{self.base_url}{shop.shop_id}")
        limit = 10
        for i in range(0, len(crawler_urls), limit):
            # get cookies and select random cookies
            self.list_headers = self.get_cookies()
            logger.info(f"Start chunk {i}")
            asyncio.run(self.main(crawler_urls[i : i + limit]))

        session.close()

    async def main(self, crawler_urls):
        random_index = random.randint(0, len(self.list_headers) - 1)
        headers = self.list_headers[random_index].value
        headers = json.loads(headers)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=100),
            headers=headers,
        ) as client:
            for query_url in crawler_urls:
                await self.task(client, query_url)
                await asyncio.sleep(1)

    async def task(self, client, query_url):
        raw_data = await self.fetch_shop_detail_from_shopee(client, query_url)
        shop_detail = await self.parse_data(raw_data)

        if shop_detail is None:
            return

        self.save_shop_detail(shop_detail)
        logger.info(
            f"Fetch and save shop detail from shopee success: {shop_detail.username}"
        )

    def get_cookies(self):
        cookie_repository = CookieRepository(session)
        cookies = cookie_repository.get_cookies(
            expired=False, type="shopee-get-shop-base"
        )
        return cookies

    async def fetch_shop_detail_from_shopee(self, client, query_url):
        try:
            async with client.get(query_url, timeout=20) as response:
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
            data = json.loads(raw_data)["data"]

            shop = self.shop_repository.model(
                shop_id=data["shopid"],
                username=data["account"]["username"],
                name=data["name"],
                cover=data["cover"] if "cover" in data else "",
                show_official_shop_label=data["show_official_shop_label"],
                is_preferred_plus_seller=data["is_preferred_plus_seller"],
                is_shopee_verified=data["is_shopee_verified"],
                chat_disabled=data["chat_disabled"],
                rating_star=data["rating_star"],
                has_decoration=data["has_decoration"],
                last_active_time=datetime.datetime.utcfromtimestamp(data["ctime"]),
                vacation=data["vacation"],
                follower_count=data["follower_count"],
                item_count=data["item_count"],
                response_rate=data["response_rate"],
                campaign_hot_deal_discount_min=data["campaign_hot_deal_discount_min"],
                shop_rating_good=data["shop_rating"]["rating_good"],
                shop_rating_normal=data["shop_rating"]["rating_normal"],
                shop_rating_bad=data["shop_rating"]["rating_bad"],
                insert_date=self.today_date,
                description=data["description"] if "description" in data else "",
            )

            return shop
        except Exception as e:
            logger.warning(f"Exception: {e} Parse shop detail failed")
            return None

    def save_shop_detail(self, shop_detail):
        try:
            self.shop_repository.update(
                shop_detail, self.shop_repository.get_shop_by_shop_id
            )
        except Exception as e:
            logger.warning(f"Exception: {shop_detail.shop_id} Save shop detail failed")
            return None


if __name__ == "__main__":
    logger.info(f"⌲ Shop detail fetched ...")
    GetShopDetail()()
