from os import path

from sqlalchemy import create_engine

from .models import Base

# init engine and create an SQLite database
db_file_path = path.join(path.dirname(__file__), 'users.db')
engine = create_engine(f'sqlite:///{db_file_path}')
# create database (if not exist)
Base.metadata.create_all(engine)
