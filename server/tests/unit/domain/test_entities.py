import unittest
from datetime import datetime, timedelta

from app.domain.entities import Admin


class AdminTestCase(unittest.TestCase):
    def test_init_with_original_password(self):
        admin_data = {'username': 'test',
                      'updated_at': datetime.now() - timedelta(
                          hours=1),
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'original_password': '123456',
                      'auth_at': datetime.now()}
        admin = Admin(**admin_data)
        self.assertEqual(admin.username, admin_data['username'])
        self.assertNotEqual(admin.password, admin_data['original_password'])
        self.assertEqual(admin.updated_at, admin_data['updated_at'])
        self.assertEqual(admin.sign, admin_data['sign'])
        self.assertEqual(admin.tip, admin_data['tip'])
        self.assertEqual(admin.auth_at, admin_data['auth_at'])

    def test_init_with_encrypted_password(self):
        admin_data = {'username': 'test',
                      'updated_at': datetime.now() - timedelta(
                          hours=1),
                      'sign': 'bullshit',
                      'tip': 'How\'s the code?',
                      'encrypted_password': '123456%DS',
                      'auth_at': datetime.now()}
        admin = Admin(**admin_data)
        self.assertEqual(admin.username, admin_data['username'])
        self.assertEqual(admin.password, admin_data['encrypted_password'])
        self.assertEqual(admin.updated_at, admin_data['updated_at'])
        self.assertEqual(admin.sign, admin_data['sign'])
        self.assertEqual(admin.tip, admin_data['tip'])
        self.assertEqual(admin.auth_at, admin_data['auth_at'])
