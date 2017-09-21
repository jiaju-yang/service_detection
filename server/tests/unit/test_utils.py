import unittest
from datetime import datetime

from app import create_app
from app.domain.utils import encrypt_with_jwt, decrypt_with_jwt


class JWTTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

    def test_encryption(self):
        with self.app.app_context():
            adict = {'name': 'psyche', 'time': datetime.now()}
            token = encrypt_with_jwt(adict)
            self.assertEqual(type(token), str)
            self.assertEqual(decrypt_with_jwt(token), adict)
