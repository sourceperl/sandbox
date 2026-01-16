#!/usr/bin/env python

"""
A very basic example of managing a user table with sqlite database.

requirements:
    $ sudo apt install python3-sqlalchemy
or 
    $ pip install sqlalchemy
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# base class for declarative class definitions
Base = declarative_base()


# define a User class that maps to a 'users' table in the database
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(16), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


# init an engine for an in-memory db (turn on echo for debug on need)
engine = create_engine(f'sqlite:///:memory:', echo=False)

# create all tables in the database (if they don't exist)
Base.metadata.create_all(engine)

# create a configured class
Session = sessionmaker(bind=engine)

# add a new user
session = Session()
for user_name in ['user1', 'user2', 'user3']:
    new_user = User(name=user_name)
    session.add(new_user)
session.commit()

# query all users
for user in session.query(User).all():
    print(user.name)
print()

# query a specific user by ID
user = session.query(User).filter_by(id=2).first()
print(user)
