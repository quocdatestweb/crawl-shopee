import os
from dotenv import load_dotenv
import pathlib

path = pathlib.Path(__file__).parent.parent
load_dotenv(path / "../.env")

PROXY = os.getenv('PROXY')

proxy= PROXY