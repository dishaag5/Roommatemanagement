from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Float, Table
from sqlalchemy.orm import relationship
from .database import Base
import uuid
household_user = Table(
    'household_user', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('household_id', Integer, ForeignKey('households.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)
    households = relationship("Household", secondary=household_user, back_populates="members")

# class Household(Base):
#     __tablename__ = 'households'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     owner_id = Column(Integer, ForeignKey('users.id'))
#     members = relationship("User", secondary=household_user, back_populates="households")


class Household(Base):
    __tablename__ = 'households'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    invite_token = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    members = relationship("User", secondary=household_user, back_populates="households")





class Chore(Base):
    __tablename__ = 'chores'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    frequency = Column(String)  # Daily, Weekly, Monthly
    household_id = Column(Integer, ForeignKey('households.id'))
    last_done_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    last_done_on = Column(Date, nullable=True)

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    description = Column(String)
    date = Column(Date)
    payer_id = Column(Integer, ForeignKey('users.id'))
    household_id = Column(Integer, ForeignKey('households.id'))




