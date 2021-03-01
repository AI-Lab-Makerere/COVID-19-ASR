from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from storage.base import BaseModel


class Station(BaseModel):
    __tablename__ = 'station_tb'
    id = Column('id', BigInteger, primary_key=True)
    name = Column('name', String)
    region = Column('region', String)
    language = Column('language', String)
    uri = Column('uri', String)
    created_at = Column('created_at', DateTime)
    updated_at = Column('updated_at', DateTime)


class Recording(BaseModel):
    __tablename__ = 'recording_tb'
    id = Column('id', BigInteger, primary_key=True)
    name = Column('name', String)
    station_id = Column('station_id', ForeignKey(Station.id), primary_key=True)
    created_at = Column('created_at', DateTime)
    finished_at = Column('finished_at', DateTime)
    size = Column('file_size', BigInteger)
    station = relationship('Station', foreign_keys='Recording.station_id')
