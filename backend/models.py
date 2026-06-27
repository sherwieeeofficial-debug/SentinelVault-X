from sqlalchemy import Column, Integer, String
from database import Base



class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String,
        unique=True
    )


    password = Column(
        String
    )



class FileRecord(Base):

    __tablename__ = "files"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String
    )


    filename = Column(
        String
    )


    file_hash = Column(
        String
    )
