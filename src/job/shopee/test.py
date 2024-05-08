import logging
import sys
import os
from datetime import datetime

# Add the root directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(utils_dir)

from config.config import settings

# Setup path to log file
settings.setup_logging('/crawler/log/test.log')

# Initialize logger
logger = logging.getLogger(__name__)

class Test:
    def __init__(self):
        logger.info("Test" + str(datetime.now()))
         
if __name__ == "__main__":
    Test()
