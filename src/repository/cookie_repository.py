from repository.base_repository import BaseRepository
from model.cookie import Cookie

class CookieRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Cookie)

    def get_cookies(self, expired=False, type="shopee-cookies-do-not-login"):
        return self.session.query(self.model).filter(self.model.expired==expired, self.model.type==type).order_by(self.model.created_at.desc()).all()