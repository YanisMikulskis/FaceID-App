import os

from sqlalchemy import create_engine, Column, Integer, String, Boolean, select, BLOB, MetaData, Date
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
import sqlite3

connect = sqlite3.connect('DataBase_Faces')
engine = create_engine('sqlite:///DataBase_Faces')
metadata = MetaData()

class Base(DeclarativeBase):
    pass

class Faces(Base):
    __tablename__ = 'Faces_codes'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(150), nullable=False)
    birthday = Column(Date, nullable=False)
    code_face = Column(BLOB, unique=True)

    def __repr__(self):
        return (f'Имя человека: {self.name}'
                f'Дата рождения: {self.birthday}'
                f'Код лица: {self.code_face}')
Base.metadata.create_all(bind=engine)
session = sessionmaker(autoflush=False, bind=engine)
db_session = session()