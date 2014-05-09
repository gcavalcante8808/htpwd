__author__ = '01388863189'
import unittest
from selenium import webdriver
from flask.ext.testing import TestCase
from flask import Flask


class UserTest(TestCase):
    def create_app(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def tearDown(self):
        self.browser.quit()

    def test_can_change_the_user_credentials_twice(self):
        """ Tests if the user can change his own password once and then
         change his new defined password."""

        # go2URL
        self.browser.get('http://localhost:8000')

        #Are we in the right page?
        self.assertIn('Apache', self.browser.title)
        self.fail('Finish the test.')



if __name__ == '__main__':
    unittest.main()