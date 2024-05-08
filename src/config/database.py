from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv
import pathlib

logger = logging.getLogger(__name__)

path = pathlib.Path(__file__).parent.parent
load_dotenv(path / "../.env")

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")
DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

try:
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    logger.info(f"Error: {str(e)}")


def check_database_connection():
    try:
        session.execute(text("SELECT 1"))
        logger.info("Database connection established successfully!")
    except Exception as e:
        logger.info(f"Error: {str(e)}")
        raise Exception("Database connection failed!")
    return True
