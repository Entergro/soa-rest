from sqlalchemy import Column, String, Integer

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(String)
    image_url = Column(String, default='')
    hashed_password = Column(String)
    wins = Column(Integer, default=0)
    fails = Column(Integer, default=0)
    count_of_session = Column(Integer, default=0)
    secs = Column(Integer, default=0)
