from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        Text, DateTime)
from sqlalchemy.orm import mapper, relationship

from app.domain.entities import Host, Service

_metadata = MetaData()

admins = Table('admins', _metadata,
               Column('id', Integer, primary_key=True),
               Column('username', String(50), unique=True, nullable=False),
               Column('password', String(200), nullable=False),
               Column('sign', String(10)),
               Column('tip', Text),
               Column('updated_at', DateTime))

hosts = Table('hosts', _metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(50), nullable=False),
              Column('detail', Text),
              Column('address', Text, nullable=False))

services = Table('services', _metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String(50), nullable=False),
                 Column('detail', Text),
                 Column('port', Integer, nullable=False),
                 Column('host_id', None, ForeignKey('hosts.id'),
                        nullable=False))

mapper(Service, services)

mapper(Host, hosts, properties={
    'services': relationship(Service, backref='host')
})


def create_all(engine):
    _metadata.create_all(engine)


def drop_all(engine):
    _metadata.drop_all(engine)
