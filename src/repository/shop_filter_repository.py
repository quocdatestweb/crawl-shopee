from repository.base_repository import BaseRepository
from model.shop_filter import ShopFilter
import logging
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

class ShopFilterRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, ShopFilter)

    def get_shop_filter_by_shop_id(self, obj: ShopFilter):
        return self.session.query(self.model).filter(self.model.shop_id==obj.shop_id).first()
    
    def bulk_insert(self, objs):
        try:
            insert_stmt = insert(self.model)
            values_list = []
            for obj in objs:
                values_list.append({
                    'shop_id': obj.shop_id,
                    'username': obj.username,
                    'is_mall': obj.is_mall
                })
            insert_stmt = insert_stmt.values(values_list)
            on_conflict_stmt = insert_stmt.on_conflict_do_update(
                index_elements=['shop_id'],
                set_={
                    'username': insert_stmt.excluded.username,
                    'is_mall': insert_stmt.excluded.is_mall
                }
            )
            self.session.execute(on_conflict_stmt)
            self.session.commit()
            logger.info(f"Database: Bulk insert success")
        except Exception as e:
            self.session.rollback()
            logger.warning(f"Database: Bulk insert failed: {e}")
            raise


        