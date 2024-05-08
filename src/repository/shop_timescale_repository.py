from repository.base_repository import BaseRepository
from model.shop_timescale import ShopTimescale

class ShopTimescaleRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, ShopTimescale)