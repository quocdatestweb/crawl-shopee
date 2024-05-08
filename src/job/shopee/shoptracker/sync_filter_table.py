import os
import sys
import logging
import asyncio
import json

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(utils_dir)

from utils.utils import timer
from config.config import settings
from repository.product_repository import ProductRepository
from repository.shop_repository import ShopRepository
from repository.shop_filter_repository import ShopFilterRepository
from repository.product_filter_repository import ProductFilterRepository

from config.database import Session
from config.timescale import Session as TimescaleSession
from config.database import check_database_connection
from config.timescale import check_timescale_connection

session = Session()
timescale_session = TimescaleSession()
settings.setup_logging("/crawler/log/sync_filter_table.log")
logger = logging.getLogger(__name__)


class SyncFilterTable:
    def __init__(self):
        check_database_connection()
        check_timescale_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.product_repository = ProductRepository(session)
        self.product_filter_repository = ProductFilterRepository(timescale_session)
        self.shop_repository = ShopRepository(session)
        self.shop_filter_repository = ShopFilterRepository(timescale_session)

    @timer
    def __call__(self):
        self.sync_shop_filter()
        self.sync_product_filter()
        session.close()

    def sync_shop_filter(self):
        shops = self.shop_repository.get_shop_tracker()
        asyncio.run(self.save_shop_filters(shops))

    async def save_shop_filters(self, shops):
        shop_filters = []
        for shop in shops:
            shop_filter = self.shop_filter_repository.model(
                shop_id=shop.shop_id,
                username=shop.username,
                is_mall=shop.show_official_shop_label,
            )
            shop_filters.append(shop_filter)
        try:
            self.shop_filter_repository.bulk_insert(shop_filters)
        except Exception as e:
            logger.warning(f"Bulk insert failed: {e}")
        logger.info(f"Saved {len(shop_filters)} shop filters")

    def sync_product_filter(self):
        products = self.product_repository.get_product_in_shoptracker()
        asyncio.run(self.save_product_filters(products))

    async def save_product_filters(self, products):
        product_filters = []
        for product in products:
            lowest_category_id = None
            if product.global_categories is not None:
                lowest_category_id = int(
                    json.loads(product.global_categories)[-1]["catid"]
                )

            product_filter = self.product_filter_repository.model(
                item_id=product.item_id,
                shop_id=product.shop_id,
                catid=product.catid,
                brand=product.brand,
                shop_location=product.shop_location,
                lowest_category_id=lowest_category_id,
            )
            product_filters.append(product_filter)
        try:
            self.product_filter_repository.bulk_insert(product_filters)
        except Exception as e:
            logger.warning(f"Bulk insert failed")
        logger.info(f"Saved {len(product_filters)} product filters")


if __name__ == "__main__":
    logger.info(f"Sync filter table ...")
    SyncFilterTable()()
