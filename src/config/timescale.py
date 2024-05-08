from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import logging
from dotenv import load_dotenv
import pathlib

logger = logging.getLogger(__name__)

path = pathlib.Path(__file__).parent.parent
load_dotenv(path / "../.env")

DB_USERNAME = os.getenv("TIMESCALE_USERNAME")
DB_PASSWORD = os.getenv("TIMESCALE_PASSWORD")
DB_HOST = os.getenv("TIMESCALE_HOST")
DB_PORT = os.getenv("TIMESCALE_PORT")
DB_DATABASE = os.getenv("TIMESCALE_DATABASE")
DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

try:
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    logger.info(f"Error: {str(e)}")


def check_timescale_connection():
    try:
        session.execute(text("SELECT 1"))
        logger.info("Timescale connection established successfully!")
    except Exception as e:
        logger.info(f"Error: {str(e)}")
        raise Exception("Timescale connection failed!")
    return True
