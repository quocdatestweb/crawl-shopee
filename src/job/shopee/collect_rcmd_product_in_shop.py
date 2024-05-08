import os
import sys
import random
import json
import logging
import asyncio
import datetime
import aiohttp
from sqlalchemy.sql import func

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(utils_dir)

from config.config import settings
from repository.product_repository import ProductRepository
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
settings.setup_logging(f'/crawler/log/{current_time}-collect_product_in_shop.log')

# Initialize logger
logger = logging.getLogger(__name__)

class CollectProductInShop:
    def __init__(self):
        # Check database connection
        check_database_connection()
        check_timescale_connection()

        # Initialize variables
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.search_item_api = "https://shopee.co.th/api/v4/shop/rcmd_items"

        self.today = datetime.datetime.now()
        self.today_date = self.today.strftime("%Y-%m-%d %H:%M:%S %z")

        self.product_repository = ProductRepository(session)
        self.shop_repository = ShopRepository(session)

        self.error_urls = []

    @timer
    def __call__(self):
        # get cookies and select random cookies
        self.list_cookies = self.get_cookies()
        
        # get all category ids
        self.list_global_category_ids = [item.global_id for item in CategoryRepository(session).list_all()]

        # crawl products in shop
        count = 0
        limit = 10
        duration = int(sys.argv[1])

        while True:
            list_shops = self.shop_repository.list_all(filter={"duration": duration, "min_item_count": "0", "limit": limit, "offset": count})

            if len(list_shops) == 0:
                break

            logger.info(f"Stating to crawl products in {len(list_shops)} shop")
            for shop in list_shops:
                logger.info(f"Shop {shop.shop_id} - {shop.name} starting: Last products in shop updated at {shop.products_in_shop_updated_at}, item count {shop.item_count}")
                crawler_urls = []

                shop_id = shop.shop_id
                if shop_id is None:
                    continue
                shop_product_count = shop.item_count
                if shop_product_count is None:
                    continue
                num = 0
                while num < shop_product_count:
                    crawler_urls.append(
                        f"{self.search_item_api}?offset={str(num)}&limit=100&bundle=shop_page_category_tab_main&sort_type=1&upstream=search&shop_id={shop_id}"
                    )
                    num += 100
                asyncio.run(self.main(crawler_urls))

                # Crawler error urls
                count = 0
                while len(self.error_urls) > 0:
                    logger.info(f"└── Start crawler {len(self.error_urls)} error urls ...")
                    error_urls = self.error_urls
                    self.error_urls = []
                    if count > 10:
                        logger.info(f"└── Cannot crawler error urls, break ...")
                        break
                    if len(error_urls) > 0:
                        asyncio.run(self.main(error_urls))
                    if len(self.error_urls) > 0:
                        logger.info(f"└── Error urls length: {len(self.error_urls)}, continue crawler error urls part {count + 1} ...")
                    count += 1

                # End crawler
                shop.products_in_shop_updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")
                self.shop_repository.update(shop, self.shop_repository.get_shop_by_shop_id)
                logger.info(f"└── End crawler {shop.name}\n\n")

            count += limit

        session.close()


    async def main(self, crawler_urls):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "referer": "https://shopee.co.th/",
            "X-Requested-With": "XMLHttpRequest",
        }
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=10),
            headers=headers,
        ) as client:
            chunk_size = 20
            chunks = [crawler_urls[i:i+chunk_size] for i in range(0, len(crawler_urls), chunk_size)]

            for chunk in chunks:
                tasks = [
                    self.task(client, query_url)
                    for query_url in chunk
                ]
                await asyncio.gather(*tasks)


    async def task(self, client, query_url):
        random_index = random.randint(0, len(self.list_cookies) - 1)
        raw_data = await self.fetch_from_shopee(client, query_url, self.list_cookies[random_index])
        if raw_data is None:
            return None
        list_product = await self.parse_data(raw_data)
        if list_product is None and len(list_product) == 0:
            return None
        self.save_list_product(list_product)


    def get_cookies(self):
        cookie_repository = CookieRepository(session)
        cookies = cookie_repository.get_cookies(expired=False, type="shopee-cookies-do-not-login")
        return cookies


    async def fetch_from_shopee(self, client, query_url, cookies):
        try:
            logger.info(f"Request {query_url} ...")
            _cookies = json.loads(cookies.value)
            async with client.get(query_url, proxy=proxy, timeout=20) as response:
                raw_data = await response.text()
                assert response.status == 200
                return raw_data
        except:
            logger.error(f"Exception: Request {query_url} failed!!!")
            self.error_urls.append(query_url)
            return None


    async def parse_data(self, raw_data):
        list_products = []
        try: 
            if not raw_data:
                return None
            info = json.loads(raw_data)
            info = info["data"]
            if info["total"] != 0:
                if "items" not in info:
                    print(info)
                for item in info["items"]:
                    item["image"] = "https://cf.shopee.co.th/file/" + item["image"]
                    dateArray = datetime.datetime.utcfromtimestamp(item["ctime"])
                    transfor_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                    product = self.product_repository.model(
                            item_id = str(item["itemid"]),
                            shop_id = item["shopid"],
                            name = item["name"],
                            catid = item["catid"],
                            image = item["image"],
                            stock = item["stock"],
                            status = item["status"],
                            ctime = item["ctime"],
                            t_ctime = transfor_time,
                            sold = item["sold"],
                            historical_sold = item["historical_sold"],
                            liked_count = item["liked_count"],
                            cmt_count = item["cmt_count"],
                            item_status = item["item_status"],
                            price = item["price"]/100000,
                            price_min = item["price_min"]/100000,
                            price_max = item["price_max"]/100000,
                            price_before_discount = item["price_before_discount"]/100000,
                            show_discount = item["show_discount"],
                            raw_discount = item["raw_discount"],
                            tier_variations_option = ",".join(item["tier_variations"][0]["options"])if item.get("tier_variations") else "",
                            rating_star_avg = item["item_rating"]["rating_star"],
                            rating_star_1 = item["item_rating"]["rating_count"][1],
                            rating_star_2 = item["item_rating"]["rating_count"][2],
                            rating_star_3 = item["item_rating"]["rating_count"][3],
                            rating_star_4 = item["item_rating"]["rating_count"][4],
                            rating_star_5 = item["item_rating"]["rating_count"][5],
                            item_type = item["item_type"],
                            is_adult = item["is_adult"],
                            has_lowest_price_guarantee = item["has_lowest_price_guarantee"], 
                            is_official_shop = item["is_official_shop"],
                            is_cc_installment_payment_eligible = item["is_cc_installment_payment_eligible"],
                            is_non_cc_installment_payment_eligible = item["is_non_cc_installment_payment_eligible"],
                            is_preferred_plus_seller = item["is_preferred_plus_seller"],
                            is_mart = item["is_mart"],
                            is_service_by_shopee = item["is_service_by_shopee"],
                            shopee_verified = item["shopee_verified"],
                            show_shopee_verified_label = item["show_shopee_verified_label"],
                            show_official_shop_label_in_title = item["show_official_shop_label_in_title"],
                            show_free_shipping = item["show_free_shipping"],
                            shop_location = item["shop_location"],
                    )
                    if str(product.catid) in self.list_global_category_ids:
                        list_products.append(product)
        except Exception as e:
            logger.warning(f"Exception: {e} Parse data failed")
        return list_products
    

    def save_list_product(self, list_product):
        if len(list_product) > 0:
            self.product_repository.bulk_insert(list_product)
            logger.info(f"└── Added {len(list_product)} products")

if __name__ == "__main__":
    logger.info(f"Product in shop fetch: ...")
    CollectProductInShop()()