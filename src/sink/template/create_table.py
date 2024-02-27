"""Berisi template query untuk create table"""

import datetime

from sqlalchemy import Table, Column
from sqlalchemy import String, Float, Integer, Boolean, \
                       BigInteger, DateTime, TIMESTAMP, \
                       VARCHAR
from sqlalchemy import MetaData
from sqlalchemy.sql import func


metadata = MetaData()

IRIS = Table(
    'iris', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('sepal_length', Float),
    Column('sepal_width', Float),
    Column('petal_length', Float),
    Column('petal_width', Float),
    Column('class', VARCHAR(80))
)

UPDATE_LOG = Table(
    'update_log', metadata,
    Column('id', BigInteger, primary_key=True, autoincrement=True),
    Column('updated_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_on', VARCHAR(80)),
    Column('last_row_added', Integer),
)