from repository.base_repository import BaseRepository
from model.shop import Shop
from typing import List
import datetime
from sqlalchemy import or_


class ShopRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Shop)

    def get_shop_by_shop_id(self, obj: Shop):
        return (
            self.session.query(self.model)
            .filter(self.model.shop_id == str(obj.shop_id))
            .first()
        )

    def get_shop_tracker(self):
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

    def list_shop_ids(self):
        return self.session.query(self.model.shop_id).all()

    def list_all(self, filter={}) -> List:
        query = self.session.query(self.model)

        if "duration" in filter:
            duration = filter["duration"]
            current_time = datetime.datetime.now()
            time_difference = datetime.timedelta(seconds=duration)
            target_time = current_time - time_difference

            query = query.filter(
                or_(
                    self.model.products_in_shop_updated_at < target_time,
                    self.model.products_in_shop_updated_at == None,
                )
            )

        if "min_item_count" in filter:
            min_item_count = filter["min_item_count"]
            query = query.filter(self.model.item_count > min_item_count)

        if "limit" in filter and "offset" in filter:
            limit = filter["limit"]
            offset = filter["offset"]
            query = query.limit(limit).offset(offset)

        return query.all()
