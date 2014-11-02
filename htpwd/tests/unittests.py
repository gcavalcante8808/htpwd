import unittest
import os


class TestHtpwd(unittest.TestCase):

    def setUp(self):
        self.test_config_file_creating()

    # def tearDown(self):
    #     os.remove('config_file_unittest.ini')

    def test_create_secret_key(self):
        from htpwd.util.base import create_secret_key
        key = create_secret_key('NewSecret')
        self.assertEqual(key, "eb1da86cd0a2981ea38d8e8f632ec451")

    def test_config_file_creating(self):
        from htpwd.util.base import create_config_file
        config = create_config_file(htfile='myhtfile', key='',
                                    target_page='http://mypage.com',
                                    regexp=r'\d{3}.',
                                    fname='config_file_unittest.ini')
        self.assertTrue(config)
        self.assertIn(config['HTPWD']['htpasswd_file'], 'myhtfile')
        self.assertIn(config['HTPWD']['secret_key'], '')
        self.assertIn(config['HTPWD']['target_page'], 'http://mypage.com')
        self.assertIn(config['HTPWD']['regexp'], '\d{3}.')

    def test_config_file_parsing(self):
        from htpwd.util.base import parse_config_file
        config = parse_config_file('config_file_unittest.ini')
        self.assertTrue(config)