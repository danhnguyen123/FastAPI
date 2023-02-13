import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UnicodeText, Float
from sqlalchemy import UniqueConstraint, Sequence
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from core.database import Base, schema_name, engine

class EventAppModel(Base):
    __table_args__ = {"schema": schema_name, 'extend_existing': True}
    __tablename__ = "event_app_realtime"
    user_id = Column(UUID, index=True)
    event_at = Column(DateTime(timezone=True), server_default=func.now())
    event_name = Column(String(128))
    title = Column(String(512))
    content = Column(String(512))
    data = Column(UnicodeText, default=None)
    message_id = Column(UUID , primary_key=True)
    app_version = Column(String(64))
    app_build = Column(Integer)
    anonymous_id = Column(UUID)

class EventWebModel(Base):
    __table_args__ = {"schema": schema_name, 'extend_existing': True}
    __tablename__ = "event_web_realtime"
    user_id = Column(UUID, index=True)
    anonymous_id = Column(UUID)
    event_at = Column(DateTime(timezone=True), server_default=func.now())
    domain = Column(String(256))
    referrer = Column(String(2048))
    path = Column(String(2048))
    search = Column(String(2048))
    title = Column(String(512))
    url = Column(String(2048))
    message_id = Column(String(50) , primary_key=True)

class EventTestModel(Base):
    __table_args__ = {"schema": schema_name, 'extend_existing': True}
    __tablename__ = "event_test_realtime"
    user_id = Column(UUID, index=True)
    event_name = Column(String(128))
    message_id = Column(String(50) , primary_key=True)

Base.metadata.create_all(bind=engine)
