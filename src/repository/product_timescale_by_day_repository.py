from repository.base_repository import BaseRepository
from model.product_timescale_by_day import ProductTimescaleByDay

class ProductTimescaleByDayRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, ProductTimescaleByDay)