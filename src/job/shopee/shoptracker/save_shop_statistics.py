import os
import sys
import logging
import asyncio
import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
sys.path.append(utils_dir)

from config.config import settings
from repository.shop_repository import ShopRepository
from repository.shop_timescale_repository import ShopTimescaleRepository
from utils.utils import timer
from config.database import Session
from config.timescale import Session as TimescaleSession
from config.database import check_database_connection
from config.timescale import check_timescale_connection

session = Session()
timescale_session = TimescaleSession()
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
settings.setup_logging(f"/crawler/log/{current_time}-save_shop_statistics.log")

logger = logging.getLogger(__name__)


class SaveShopStatistics:
    def __init__(self):
        check_database_connection()
        check_timescale_connection()
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.shop_repository = ShopRepository(session)
        self.shop_timescale_repository = ShopTimescaleRepository(timescale_session)

    @timer
    def __call__(self):
        shops = self.shop_repository.get_shop_tracker()
        if len(shops) == 0:
            logger.info(f"No shop in shoptracker")
            return
        asyncio.run(self.save_shop_statistics(shops))
        session.close()
        timescale_session.close()

    async def save_shop_statistics(self, shops):
        shop_timescales = []
        for shop in shops:
            shop_timescale = self.shop_timescale_repository.model(
                time=datetime.datetime.now(),
                shop_id=shop.shop_id,
                rating_star=shop.rating_star,
                follower_count=shop.follower_count,
                item_count=shop.item_count,
                response_rate=shop.response_rate,
                campaign_hot_deal_discount_min=shop.campaign_hot_deal_discount_min,
                shop_rating_good=shop.shop_rating_good,
                shop_rating_normal=shop.shop_rating_normal,
                shop_rating_bad=shop.shop_rating_bad,
            )
            shop_timescales.append(shop_timescale)
        self.shop_timescale_repository.create_all(shop_timescales)
        logger.info(f"Saved {len(shop_timescales)} shop statistics")


if __name__ == "__main__":
    SaveShopStatistics()()
