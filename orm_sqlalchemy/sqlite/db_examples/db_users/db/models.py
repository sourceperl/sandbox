from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """represents a system user"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    # relationship using mapped type hints for list autocomplete
    addresses: Mapped[List['Address']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<User(id={self.id}, name={self.name!r})>'


class Address(Base):
    """represents an email address linked to a user"""
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(100), unique=True)

    # foreign key using mapped_column
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # back relationship to user
    user: Mapped['User'] = relationship(back_populates='addresses')

    def __repr__(self) -> str:
            return f'<Address(id={self.id}, email={self.email_address!r}, user_id={self.user_id})>'