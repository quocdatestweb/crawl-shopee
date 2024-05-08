from repository.base_repository import BaseRepository
from model.product_filter import ProductFilter
import logging
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

class ProductFilterRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, ProductFilter)

    def get_product_filter_by_item_id(self, obj: ProductFilter):
        return self.session.query(self.model).filter(self.model.item_id==obj.item_id).first()

    def bulk_insert(self, objs):
        try:
            insert_stmt = insert(self.model)
            values_list = []
            for obj in objs:
                values_list.append({
                    'item_id': obj.item_id,
                    'shop_id': obj.shop_id,
                    'catid': obj.catid,
                    'brand': obj.brand,
                    'shop_location': obj.shop_location,
                    'lowest_category_id': obj.lowest_category_id,
                })
            insert_stmt = insert_stmt.values(values_list)
            on_conflict_stmt = insert_stmt.on_conflict_do_update(
                index_elements=['item_id'],
                set_={
                    'catid': insert_stmt.excluded.catid,
                    'brand': insert_stmt.excluded.brand,
                    'shop_location': insert_stmt.excluded.shop_location,
                    'lowest_category_id': insert_stmt.excluded.lowest_category_id,
                }
            )
            self.session.execute(on_conflict_stmt)
            self.session.commit()
            logger.info(f"Database: Bulk insert success")
        except Exception as e:
            self.session.rollback()
            logger.warning(f"Database: Bulk insert failed: {e}")
            raise