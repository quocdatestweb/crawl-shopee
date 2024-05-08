from sqlalchemy.orm import Session
from typing import List
import logging

logger = logging.getLogger(__name__)

class BaseRepository:
    def __init__(self, session: Session, model):
        self.session = session
        self.model = model
    
    def create(self, obj):
        try: 
            self.session.add(obj)
            self.session.commit()
            logger.info(f"Database: Create success")
        except:
            self.session.rollback()
            logger.warning("Database: Create failed")
            raise

    def create_all(self, objs: List):
        try:
            self.session.add_all(objs)
            self.session.commit()
            logger.info(f"Database: Create all success")
        except:
            self.session.rollback()
            logger.warning("Database: Create all failed")
            raise
    
    def read(self, obj_id):
        return self.session.query(self.model).filter_by(id=obj_id).first()
    
    def update(self, obj, fn_filter):
        try: 
            new_data = fn_filter(obj)
            update_attrs = [attr for attr in obj.__dict__ if not attr.startswith('_')]
            for attr in update_attrs:
                setattr(new_data, attr, getattr(obj, attr))
            self.session.commit()
            logger.info(f"Database: Update success")
            return new_data
        except Exception as e:
            logger.warning(f"Database: Update failed: {e}")
            self.session.rollback()
            raise
    
    def update_all(self, objs: List, fn_filter):
        try:
            for obj in objs:
                new_data = fn_filter(obj)
                update_attrs = [attr for attr in obj.__dict__ if not attr.startswith('_')]
                for attr in update_attrs:
                    setattr(new_data, attr, getattr(obj, attr))
            self.session.commit()
            logger.info(f"Database: Update all success")
        except Exception as e:
            self.session.rollback()
            logger.warning("Database: Update all failed")
            logger.warning(e)

    def upsert(self, obj, fn_filter):
        try:
            self.create(obj)
        except:
            self.session.rollback()
            self.update(obj, fn_filter)

    def upsert_all(self, objs: List, fn_filter):
        try:
            self.create_all(objs)
        except:
            self.session.rollback()
            self.update_all(objs, fn_filter)

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()
    
    def list_all(self):
        return self.session.query(self.model).all()
    
    def get_list(self, limit: int = 10, offset: int = 10):
        return self.session.query(self.model).limit(limit).offset(offset).all()
