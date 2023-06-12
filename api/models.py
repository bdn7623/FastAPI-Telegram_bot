from database import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Table,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


group_message_table = Table(
    "group_message_table",
    Base.metadata,
    Column("message_id", ForeignKey("messages.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)

group_lector_table = Table(
    "group_lector_table",
    Base.metadata,
    Column("lector_id", ForeignKey("lectors.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(150))
    lectors = relationship("Lector",
                              secondary=group_lector_table)
    
    messages = relationship("Message",
                              secondary=group_message_table)
    
    def __str__(self):
        return self.group_name



class Lector(Base):
    __tablename__ = "lectors"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    groups = relationship("Group",
                            secondary=group_lector_table)
    def __str__(self):
        return self.username



class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    text = Column(String(100))
    link = Column(String(100))
    date_time = Column(DateTime, default=datetime.utcnow)
    groups = relationship("Group",
                            secondary=group_message_table)
    def __str__(self):
        return self.text
