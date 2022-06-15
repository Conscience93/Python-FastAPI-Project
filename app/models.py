
from email.policy import default

from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.sql.expression import TextClause

from .database import Base

class Post(Base):
    #Note: If the table already exists, it's not going to modify the existing table.
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=TextClause('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, UniqueConstraint=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=TextClause('now()'))
