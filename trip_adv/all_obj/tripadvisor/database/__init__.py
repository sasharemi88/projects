from os.path import dirname

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.utils.conf import closest_scrapy_cfg


work_dir = dirname(closest_scrapy_cfg())

engine = create_engine(f'sqlite:///{work_dir}/database.sqlite3',
                       connect_args={'check_same_thread': False},)

Session = sessionmaker(engine, autoflush=False, autocommit=False)