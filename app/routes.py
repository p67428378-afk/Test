from flask import Blueprint, jsonify, request
from .services import get_all_rooms, get_room_by_id, update_room_status, initialize_room_statuses, create_initial_rooms
from .models import db

room_bp = Blueprint('room_bp', __name__)

@room_bp.before_app_first_request
def setup_data():
    with db.session.begin():
        initialize_room_statuses()
        create_initial_rooms()

@room_bp.route('/rooms', methods=['GET'])
def list_rooms():
    rooms = get_all_rooms()
    return jsonify([
        {
            'room_id': room.room_id,
            'room_number': room.room_number,
            'room_type': room.room_type,
            'capacity': room.capacity,
            'current_status': room.current_status.status_name,
            'last_updated_at': room.last_updated_at.isoformat()
        }
        for room in rooms
    ])

@room_bp.route('/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    room = get_room_by_id(room_id)
    if not room:
        return jsonify({'message': 'Room not found'}), 404
    return jsonify({
        'room_id': room.room_id,
        'room_number': room.room_number,
        'room_type': room.room_type,
        'capacity': room.capacity,
        'current_status': room.current_status.status_name,
        'last_updated_at': room.last_updated_at.isoformat()
    })

@room_bp.route('/rooms/<room_id>/status', methods=['PUT'])
def change_room_status(room_id):
    data = request.get_json()
    new_status_name = data.get('status')
    reason = data.get('reason')
    changed_by_user_id = data.get('changed_by_user_id', 'system') # Placeholder for actual user ID

    if not new_status_name:
        return jsonify({'message': 'Status is required'}), 400

    room, error = update_room_status(room_id, new_status_name, reason, changed_by_user_id)
    if error:
        return jsonify({'message': error}), 400
    if not room:
        return jsonify({'message': 'Room not found'}), 404

    return jsonify({
        'room_id': room.room_id,
        'room_number': room.room_number,
        'current_status': room.current_status.status_name,
        'message': 'Room status updated successfully'
    })
