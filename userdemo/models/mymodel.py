from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date,
    String
)

from .meta import Base


class User(Base):
    __tablename__ = 'entries'
    id = Column(Integer)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    username = Column(Unicode, primary_key=True)
    email = Column(String)
    food = Column(Unicode)
    password = Column(Unicode) #! should be something else like a special type for passwords
    creation_date = Column(Date)


Index('index', User.username, unique=True, mysql_length=255)
