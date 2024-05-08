from repository.base_repository import BaseRepository
from model.product_timescale import ProductTimescale

class ProductTimescaleRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, ProductTimescale)