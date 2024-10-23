import unittest
import socket
from unittest.mock import Mock
from my_socket import MySocket

class TestMySocket(unittest.TestCase):

    def setUp(self):
        self.my_socket = MySocket(5, 1)

    def test_connect_timeout(self):
        with self.assertRaises(TimeoutError):
            self.my_socket.connect('stackoverflow.nordquant.com', 2731)

    def test_connect_gaierror(self):
        with self.assertRaises(socket.gaierror):
            self.my_socket.connect('stackoverflow.nordquantasd.com', 2730)

    def test_receive_raises_error(self):
        self.my_socket.sock = Mock()
        self.my_socket.connect('stackoverflow.nordquant.com', 2730)
        self.my_socket.sock.recv.return_value = None
        with self.assertRaises(RuntimeError):
            self.my_socket.receive()

if __name__ == '__main__':
    unittest.main()