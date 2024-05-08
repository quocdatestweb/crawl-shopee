from repository.base_repository import BaseRepository
from model.product import Product
from typing import List
import logging
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
from sqlalchemy import or_


logger = logging.getLogger(__name__)


class ProductRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Product)

    def get_product_by_item_id(self, obj: Product):
        return (
            self.session.query(self.model)
            .filter(self.model.item_id == obj.item_id)
            .first()
        )

    def get_list(self, limit: int = 10, offset: int = 0, filter={}) -> List:
        query = self.session.query(self.model)
        if "local_categories" in filter:
            query = query.filter(
                self.model.local_categories == filter["local_categories"]
            )
        query = query.order_by(self.model.created_at.asc()).limit(limit).offset(offset)
        return query.all()

    def get_product_in_shoptracker(
        self,
    ) -> List:
        query = self.session.query(self.model)
        query = query.filter(
            or_(
                self.model.shop_id == "82590052",
                self.model.shop_id == "78516148",
                self.model.shop_id == "29668843",
                self.model.shop_id == "373514360",
                self.model.shop_id == "29667634",
                self.model.shop_id == "224882570",
                self.model.shop_id == "123415275",
                self.model.shop_id == "242198953",
                self.model.shop_id == "530221668",
                self.model.shop_id == "152492041", 
                self.model.shop_id == "261911756"
            )
        )
        return query.all()

    def bulk_insert(self, objs):
        if len(objs) == 0:
            return
        try:
            insert_stmt = insert(self.model)
            values_list = []
            for obj in objs:
                values_list.append(
                    {
                        "item_id": obj.item_id,
                        "shop_id": obj.shop_id,
                        "name": obj.name,
                        "catid": obj.catid,
                        "image": obj.image,
                        "stock": obj.stock,
                        "status": obj.status,
                        "ctime": obj.ctime,
                        "t_ctime": obj.t_ctime,
                        "sold": obj.sold,
                        "historical_sold": obj.historical_sold,
                        "liked_count": obj.liked_count,
                        "cmt_count": obj.cmt_count,
                        "item_status": obj.item_status,
                        "price": obj.price,
                        "price_min": obj.price_min,
                        "price_max": obj.price_max,
                        "price_before_discount": obj.price_before_discount,
                        "show_discount": obj.show_discount,
                        "raw_discount": obj.raw_discount,
                        "tier_variations_option": obj.tier_variations_option,
                        "rating_star_avg": obj.rating_star_avg,
                        "rating_star_1": obj.rating_star_1,
                        "rating_star_2": obj.rating_star_2,
                        "rating_star_3": obj.rating_star_3,
                        "rating_star_4": obj.rating_star_4,
                        "rating_star_5": obj.rating_star_5,
                        "item_type": obj.item_type,
                        "is_adult": obj.is_adult,
                        "has_lowest_price_guarantee": obj.has_lowest_price_guarantee,
                        "is_official_shop": obj.is_official_shop,
                        "is_cc_installment_payment_eligible": obj.is_cc_installment_payment_eligible,
                        "is_non_cc_installment_payment_eligible": obj.is_non_cc_installment_payment_eligible,
                        "is_preferred_plus_seller": obj.is_preferred_plus_seller,
                        "is_mart": obj.is_mart,
                        "is_service_by_shopee": obj.is_service_by_shopee,
                        "shopee_verified": obj.shopee_verified,
                        "show_shopee_verified_label": obj.show_shopee_verified_label,
                        "show_official_shop_label_in_title": obj.show_official_shop_label_in_title,
                        "show_free_shipping": obj.show_free_shipping,
                        "shop_location": obj.shop_location,
                        "updated_at": datetime.now(),
                    }
                )
            insert_stmt = insert_stmt.values(values_list)
            on_conflict_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["item_id"],
                set_={
                    "shop_id": insert_stmt.excluded.shop_id,
                    "name": insert_stmt.excluded.name,
                    "catid": insert_stmt.excluded.catid,
                    "image": insert_stmt.excluded.image,
                    "stock": insert_stmt.excluded.stock,
                    "status": insert_stmt.excluded.status,
                    "ctime": insert_stmt.excluded.ctime,
                    "t_ctime": insert_stmt.excluded.t_ctime,
                    "sold": insert_stmt.excluded.sold,
                    "historical_sold": insert_stmt.excluded.historical_sold,
                    "liked_count": insert_stmt.excluded.liked_count,
                    "cmt_count": insert_stmt.excluded.cmt_count,
                    "item_status": insert_stmt.excluded.item_status,
                    "price": insert_stmt.excluded.price,
                    "price_min": insert_stmt.excluded.price_min,
                    "price_max": insert_stmt.excluded.price_max,
                    "price_before_discount": insert_stmt.excluded.price_before_discount,
                    "show_discount": insert_stmt.excluded.show_discount,
                    "raw_discount": insert_stmt.excluded.raw_discount,
                    "tier_variations_option": insert_stmt.excluded.tier_variations_option,
                    "rating_star_avg": insert_stmt.excluded.rating_star_avg,
                    "rating_star_1": insert_stmt.excluded.rating_star_1,
                    "rating_star_2": insert_stmt.excluded.rating_star_2,
                    "rating_star_3": insert_stmt.excluded.rating_star_3,
                    "rating_star_4": insert_stmt.excluded.rating_star_4,
                    "rating_star_5": insert_stmt.excluded.rating_star_5,
                    "item_type": insert_stmt.excluded.item_type,
                    "is_adult": insert_stmt.excluded.is_adult,
                    "has_lowest_price_guarantee": insert_stmt.excluded.has_lowest_price_guarantee,
                    "is_official_shop": insert_stmt.excluded.is_official_shop,
                    "is_cc_installment_payment_eligible": insert_stmt.excluded.is_cc_installment_payment_eligible,
                    "is_non_cc_installment_payment_eligible": insert_stmt.excluded.is_non_cc_installment_payment_eligible,
                    "is_preferred_plus_seller": insert_stmt.excluded.is_preferred_plus_seller,
                    "is_mart": insert_stmt.excluded.is_mart,
                    "is_service_by_shopee": insert_stmt.excluded.is_service_by_shopee,
                    "shopee_verified": insert_stmt.excluded.shopee_verified,
                    "show_shopee_verified_label": insert_stmt.excluded.show_shopee_verified_label,
                    "show_official_shop_label_in_title": insert_stmt.excluded.show_official_shop_label_in_title,
                    "show_free_shipping": insert_stmt.excluded.show_free_shipping,
                    "shop_location": insert_stmt.excluded.shop_location,
                    "updated_at": insert_stmt.excluded.updated_at,
                },
            )
            self.session.execute(on_conflict_stmt)
            self.session.commit()
            logger.info(f"Database: Bulk insert success")
        except Exception as e:
            self.session.rollback()
            logger.warning(f"Database: Bulk insert failed: {e}")
            raise
