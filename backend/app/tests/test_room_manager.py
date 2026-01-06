import unittest

from app.routes.websocket import RoomManager

class TestRoomManager(unittest.TestCase):
    def setUp(self):
        self.room_mamger = RoomManager()

    def test_generate_code(self):
        print(self.room_mamger.generate_room_code())

if __name__ == "__main__":
    unittest.main()