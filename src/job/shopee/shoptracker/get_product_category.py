import os
import sys
import json
import logging
import asyncio
import aiohttp
import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(utils_dir)

from config.config import settings
from utils.utils import timer
from repository.product_repository import ProductRepository
from config.database import Session
from config.database import check_database_connection
from config.timescale import check_timescale_connection
from config.proxy import proxy

# Initialize the session
session = Session()

# Setup path to log file
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(
    f"/crawler/log/{current_time}-shoptracker-get_product_category.log"
)

# Initialize logger
logger = logging.getLogger(__name__)


class GetProductCategory:
    def __init__(self):
        check_database_connection()
        check_timescale_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.search_item_api = "https://shopee.co.th/api/v4/item/get"
        self.product_repository = ProductRepository(session)

    @timer
    def __call__(self):
        count = 0
        limit = 10

        while True:
            # Get list of products that have local_categories is None
            list_products = self.product_repository.get_list(
                offset=count, limit=limit, filter={"local_categories": None}
            )

            # If there is no product left, break the loop
            if len(list_products) == 0:
                break

            # Increase the offset
            count += limit

            # Create list of crawler urls
            crawler_urls = []
            for product in list_products:
                shop_id = product.shop_id
                item_id = product.item_id
                crawler_urls.append(
                    f"{self.search_item_api}?itemid={item_id}&shopid={shop_id}"
                )

            # Crawl with list of crawler urls
            asyncio.run(self.main(crawler_urls))

        session.close()

    async def main(self, crawler_urls):
        # Copy curl from shopee, import curl to postman, export to python, then copy the code below
        headers = {
            "authority": "shopee.co.th",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "referer": "https://shopee.co.th/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "x-sz-sdk-version": "2.8.1-2@1.2.1",
        }
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, limit=3),
            headers=headers,
        ) as client:
            updated_list_products = []

            # Crawling multiple urls at the same time
            tasks = [
                self.task(client, query_url, updated_list_products)
                for query_url in crawler_urls
            ]
            await asyncio.gather(*tasks)
            logger.info(
                f"Added {len(updated_list_products)} products to updated_list_products"
            )

            # Save to database
            await self.save(updated_list_products)
            logger.info(
                f"Updated {len(updated_list_products)} products to database successfully"
            )

    async def task(self, client, query_url, updated_list_products):
        # Fetch data
        raw_data = await self.fetch(client, query_url)

        # Parse data and add to updated_list_products
        product_detail = await self.parse_data(raw_data)
        if product_detail is None:
            return
        updated_list_products.append(product_detail)
        logger.info(f"Added {product_detail.item_id} to updated_list_products")

    async def fetch(self, client, query_url):
        try:
            async with client.get(query_url, proxy=proxy, timeout=20) as response:
                raw_data = await response.text()
                assert response.status == 200
                return raw_data
        except:
            logger.warning(
                f"Exception: {query_url} Fetch shop detail from shopee failed"
            )
            return None

    async def save(self, updated_list_products):
        if len(updated_list_products) > 0:
            self.product_repository.update_all(
                updated_list_products, self.product_repository.get_product_by_item_id
            )

    async def parse_data(self, raw_data):
        try:
            data = json.loads(raw_data)
            data = data["data"]
            product = self.product_repository.model(
                item_id=str(data["itemid"]),
                local_categories=json.dumps(data["fe_categories"]),
                global_categories=json.dumps(data["categories"]),
                brand=data["brand"],
            )
            return product
        except Exception:
            logger.warning(
                f"Exception: {raw_data} Parse product detail from shopee failed"
            )
            return None


if __name__ == "__main__":
    logger.info(f"Get product category ...")
    GetProductCategory()()
