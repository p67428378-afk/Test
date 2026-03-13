import os
import unittest
from app import create_app
from app.models import db, Room, RoomStatus, RoomStatusLog
from app.services import initialize_room_statuses, create_initial_rooms

class RoomStatusTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SECRET_KEY'] = 'test_secret'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        initialize_room_statuses()
        create_initial_rooms()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_list_rooms(self):
        response = self.client.get('/rooms')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertIn('room_id', response.json[0])
        self.assertIn('current_status', response.json[0])

    def test_get_single_room(self):
        # Get a room_id from the initial rooms
        room = Room.query.first()
        response = self.client.get(f'/rooms/{room.room_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['room_id'], room.room_id)

    def test_update_room_status_vacant_to_occupied(self):
        vacant_room = Room.query.filter(Room.current_status.has(status_name='vacant')).first()
        if not vacant_room:
            self.fail("No vacant room found for testing.")

        response = self.client.put(
            f'/rooms/{vacant_room.room_id}/status',
            json={'status': 'occupied', 'reason': 'Guest checked in', 'changed_by_user_id': 'test_user'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['current_status'], 'occupied')

        # Verify log entry
        log = RoomStatusLog.query.filter_by(room_id=vacant_room.room_id).order_by(RoomStatusLog.change_timestamp.desc()).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.new_status.status_name, 'occupied')

    def test_update_room_status_out_of_order_to_occupied_invalid(self):
        ooo_room = Room.query.filter(Room.current_status.has(status_name='out-of-order')).first()
        if not ooo_room:
            self.fail("No out-of-order room found for testing.")

        response = self.client.put(
            f'/rooms/{ooo_room.room_id}/status',
            json={'status': 'occupied', 'reason': 'Maintenance complete, guest checking in', 'changed_by_user_id': 'test_user'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot transition directly', response.json['message'])

    def test_update_room_status_out_of_order_to_vacant_then_occupied(self):
        ooo_room = Room.query.filter(Room.current_status.has(status_name='out-of-order')).first()
        if not ooo_room:
            self.fail("No out-of-order room found for testing.")

        # Transition to vacant first
        response_vacant = self.client.put(
            f'/rooms/{ooo_room.room_id}/status',
            json={'status': 'vacant', 'reason': 'Maintenance complete, cleaned', 'changed_by_user_id': 'test_user'}
        )
        self.assertEqual(response_vacant.status_code, 200)
        self.assertEqual(response_vacant.json['current_status'], 'vacant')

        # Then transition to occupied
        response_occupied = self.client.put(
            f'/rooms/{ooo_room.room_id}/status',
            json={'status': 'occupied', 'reason': 'Guest checked in', 'changed_by_user_id': 'test_user'}
        )
        self.assertEqual(response_occupied.status_code, 200)
        self.assertEqual(response_occupied.json['current_status'], 'occupied')

if __name__ == '__main__':
    unittest.main()