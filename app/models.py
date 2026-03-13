from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class RoomStatus(db.Model):
    __tablename__ = 'room_status'
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    rooms = db.relationship('Room', backref='current_status', lazy=True)
    logs_old = db.relationship('RoomStatusLog', foreign_keys='RoomStatusLog.old_status_id', backref='old_status', lazy=True)
    logs_new = db.relationship('RoomStatusLog', foreign_keys='RoomStatusLog.new_status_id', backref='new_status', lazy=True)

    def __repr__(self):
        return f"<RoomStatus {self.status_name}>"

class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    current_status_id = db.Column(db.Integer, db.ForeignKey('room_status.status_id'), nullable=False)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    logs = db.relationship('RoomStatusLog', backref='room', lazy=True)

    def __repr__(self):
        return f"<Room {self.room_number} - {self.current_status.status_name}>"

class RoomStatusLog(db.Model):
    __tablename__ = 'room_status_logs'
    log_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id = db.Column(db.String(36), db.ForeignKey('rooms.room_id'), nullable=False)
    old_status_id = db.Column(db.Integer, db.ForeignKey('room_status.status_id'), nullable=False)
    new_status_id = db.Column(db.Integer, db.ForeignKey('room_status.status_id'), nullable=False)
    changed_by_user_id = db.Column(db.String(36)) # Assuming UUID for user IDs
    change_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.Text)

    def __repr__(self):
        return f"<RoomStatusLog {self.room.room_number}: {self.old_status.status_name} -> {self.new_status.status_name} at {self.change_timestamp}>"
