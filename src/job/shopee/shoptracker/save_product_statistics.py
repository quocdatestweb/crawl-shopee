import os
import sys
import logging
import asyncio
import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(utils_dir)

from utils.utils import timer
from config.config import settings
from repository.product_repository import ProductRepository
from repository.product_timescale_repository import ProductTimescaleRepository
from config.database import Session
from config.timescale import Session as TimescaleSession
from config.database import check_database_connection
from config.timescale import check_timescale_connection

session = Session()
timescale_session = TimescaleSession()

current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(f"/crawler/log/{current_time}-save_product_statistics.log")
logger = logging.getLogger(__name__)


class SaveProductStatistics:
    def __init__(self):
        check_database_connection()
        check_timescale_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.product_repository = ProductRepository(session)
        self.product_timescale_repository = ProductTimescaleRepository(
            timescale_session
        )

    @timer
    def __call__(self):
        products = self.product_repository.get_product_in_shoptracker()
        if len(products) == 0:
            logger.info(f"No product in shoptracker")
            return
        asyncio.run(self.save_product_statistics(products))
        session.close()
        timescale_session.close()

    async def save_product_statistics(self, products):
        product_timescales = []
        for product in products:
            logger.info(
                f"Saving product statistics: {product.item_id} in shop {product.shop_id}"
            )
            product_timescale = self.product_timescale_repository.model(
                time=datetime.datetime.now(),
                product_id=product.item_id,
                stock=product.stock,
                sold=product.sold,
                historical_sold=product.historical_sold,
                liked_count=product.liked_count,
                cmt_count=product.cmt_count,
                price=product.price,
                price_min=product.price_min,
                price_max=product.price_max,
                price_before_discount=product.price_before_discount,
                show_discount=product.show_discount,
                raw_discount=product.raw_discount,
                rating_star_1=product.rating_star_1,
                rating_star_2=product.rating_star_2,
                rating_star_3=product.rating_star_3,
                rating_star_4=product.rating_star_4,
                rating_star_5=product.rating_star_5,
            )
            product_timescales.append(product_timescale)
        self.product_timescale_repository.create_all(product_timescales)
        logger.info(f"Saved {len(product_timescales)} product statistics")


if __name__ == "__main__":
    logger.info(f"Saving product statistics ...")
    SaveProductStatistics()()
