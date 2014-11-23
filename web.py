from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config

Base = declarative_base()

class Zipcode(Base):
	__tablename__ = "zipcodes"
	id = Column(Integer, primary_key=True)
	code = Column(Integer, unique=True)
	lat_deg = Column(Integer)
	lat_min = Column(Integer)
	lat_sec = Column(Float)
	lon_deg = Column(Integer)
	lon_min = Column(Integer)
	lon_sec = Column(Float)

engine = create_engine(config.db)
Base.metadata.create_all(engine)

session = sessionmaker()
session.configure(autoflush=True, autocommit=False, bind=engine)
db = session()