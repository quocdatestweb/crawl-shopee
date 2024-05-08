from repository.base_repository import BaseRepository
from model.category import Category

class CategoryRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Category)