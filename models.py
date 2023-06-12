from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

group_lector_table = db.Table(
    "group_lector_table",
    db.Column("lector_id", db.ForeignKey("lectors.id"), primary_key=True),
    db.Column("group_id", db.ForeignKey("groups.id"), primary_key=True),
)

group_message_table = db.Table(
    "group_message_table",
    db.Column("message_id", db.ForeignKey("messages.id"), primary_key=True),
    db.Column("group_id", db.ForeignKey("groups.id"), primary_key=True),
)

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(150))
    lectors = db.relationship("Lector",
                              secondary=group_lector_table)
    messages = db.relationship("Message",
                              secondary=group_message_table)
    def __str__(self):
        return self.group_name

class Lector(db.Model):
    __tablename__ = "lectors"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    groups = db.relationship("Group",
                            secondary=group_lector_table)
    def __str__(self):
        return self.username
    
class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    link = db.Column(db.String(100))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    groups = db.relationship("Group",
                            secondary=group_message_table)
    def __str__(self):
        return self.text
