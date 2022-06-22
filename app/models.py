
from email.policy import default
from enum import unique

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.expression import TextClause
from sqlalchemy.orm import relationship

from .database import Base

class Post(Base):
    #Note: If the table already exists, it's not going to modify the existing table. There's no database migration tool function yet.
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=TextClause('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # ForeignKey("users.id", ondelete="CASCADE")  name get from __tablename__, CASCADE means when user is deleted, the post will be deleted as well.

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=TextClause('now()'))

class Vote(Base):
    __tablename__="votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
