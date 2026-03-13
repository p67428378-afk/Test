from .models import db, Room, RoomStatus, RoomStatusLog
from sqlalchemy.exc import IntegrityError

def get_all_rooms():
    return Room.query.all()

def get_room_by_id(room_id):
    return Room.query.get(room_id)

def update_room_status(room_id, new_status_name, reason=None, changed_by_user_id=None):
    room = Room.query.get(room_id)
    if not room:
        return None, "Room not found"

    new_status = RoomStatus.query.filter_by(status_name=new_status_name).first()
    if not new_status:
        return None, f"Invalid status: {new_status_name}"

    old_status = room.current_status

    # HLD-defined transition rule: cannot go directly from 'out-of-order' to 'occupied'
    if old_status.status_name == 'out-of-order' and new_status_name == 'occupied':
        return None, "Cannot transition directly from 'out-of-order' to 'occupied'. Must first be 'vacant'."

    # Log the status change
    log = RoomStatusLog(
        room_id=room.room_id,
        old_status_id=old_status.status_id,
        new_status_id=new_status.status_id,
        changed_by_user_id=changed_by_user_id, # In a real app, this would come from authenticated user
        reason=reason
    )
    db.session.add(log)

    room.current_status = new_status
    db.session.commit()
    return room, None

def initialize_room_statuses():
    # Ensure default statuses exist
    statuses = ['vacant', 'occupied', 'out-of-order']
    for status_name in statuses:
        if not RoomStatus.query.filter_by(status_name=status_name).first():
            status = RoomStatus(status_name=status_name, description=f"{status_name.capitalize()} room status")
            db.session.add(status)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

def create_initial_rooms():
    # Create some dummy rooms if none exist
    if Room.query.count() == 0:
        vacant_status = RoomStatus.query.filter_by(status_name='vacant').first()
        occupied_status = RoomStatus.query.filter_by(status_name='occupied').first()
        ooo_status = RoomStatus.query.filter_by(status_name='out-of-order').first()

        if vacant_status and occupied_status and ooo_status:
            rooms_data = [
                {'room_number': '101', 'room_type': 'Standard', 'capacity': 2, 'current_status': occupied_status},
                {'room_number': '102', 'room_type': 'Standard', 'capacity': 2, 'current_status': vacant_status},
                {'room_number': '103', 'room_type': 'Deluxe', 'capacity': 3, 'current_status': ooo_status},
                {'room_number': '201', 'room_type': 'Suite', 'capacity': 4, 'current_status': vacant_status},
            ]
            for data in rooms_data:
                room = Room(
                    room_number=data['room_number'],
                    room_type=data['room_type'],
                    capacity=data['capacity'],
                    current_status=data['current_status']
                )
                db.session.add(room)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

