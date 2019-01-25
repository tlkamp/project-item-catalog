from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from flask_login import UserMixin
import os

Base = declarative_base()


# use UserMixin from flask_login to get those sweet, sweet defaults
class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True, index=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    desc = Column(String(250))
    last_updated = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    category = relationship(Category)
    category_id = Column(Integer, ForeignKey('category.id'))

    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.desc,
            'last_updated': self.last_updated.strftime('%Y-%m-%d %H:%M'),
            'category': self.category.name,
            'user': self.user_id
        }


# We always want the metadata created if it hasn't been.
db_string = os.environ.get('DB_STRING')
engine = create_engine(db_string)
Base.metadata.create_all(engine)
