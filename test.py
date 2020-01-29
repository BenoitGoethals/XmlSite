import os
import sys
import Domain as Domain
from sqlalchemy import Column, ForeignKey, Integer, String, MetaData,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

metadata = MetaData()
books = Table('book', metadata,
  Column('id', Integer, primary_key=True),
  Column('title', String),
  Column('primary_author', String),
)

engine = create_engine('sqlite:///bookstore.db')
metadata.create_all(engine)