__author__ = '01388863189'
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

        # Is Any box to enter the username available?
        userbox = self.browser.find_element_by_id('name')
        self.assertEqual(userbox.get_attribute('name'), 'name')

        #Time to enter the username that was previously created by an admin
        userbox.send_keys('12345678901@test.com')

        # Is there any box to enter our current password?
        passwd = self.browser.find_element_by_id('passwd')
        self.assertTrue(passwd)

        # Time to enter our current password into the right field:
        passwd.send_keys('Test123@enterprise')

        # Is there any box to send the new password value?
        newpwd = self.browser.find_element_by_id('newpwd')
        self.assertTrue(newpwd)

        # Time to enter our new password.
        newpwd.send_keys('htpwd123@enterprise')

        # Is there any box to confirm the new password?
        newpwd2 = self.browser.find_element_by_id('newpwd2')
        self.assertTrue(newpwd2)

        #Time to confirm our new password and hit enter to send all changes.
        newpwd2.send_keys('htpwd123@enterprise')
        newpwd2.send_keys(Keys.ENTER)

        # now a congratulations page will be presented with a link for the
        # environment that uses this new credential.
        self.assertIn('http://localhost:8000/changed', self.browser.current_url)

if __name__ == '__main__':
    unittest.main()