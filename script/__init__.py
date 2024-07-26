import os
from datetime import datetime

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# generate a DATA_VERSION (YYYYMMDDHH)
DATA_VERSION = datetime.strftime(datetime.utcnow(), '%Y%m%d%H')

print(DATA_VERSION)
