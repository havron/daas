from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import os
import socket

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'

class SeleniumTests(StaticLiveServerTestCase):
    fixtures = ['././models/db.json']

    #live_server_url = 'http://{}:8000'.format(
     #   socket.gethostbyname(socket.gethostname()))

    @classmethod
    def setUpClass(self):
        
        #super(SeleniumTests, cls).setUpClass()
        #System.setProperty("webdriver.gecko.driver", "C:\Users\Monica\Downloads\geckodriver-v0.11.1-win64")
        #cls.selenium = WebDriver()
        #cls.selenium.implicitly_wait(10)
        
        #setting.DEBUG = True
        self.browser = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

    @classmethod
    def tearDownClass(self):
        '''
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()
        '''
        self.browser.quit()
        super(SeleniumTests, self).tearDownClass()

    def test_1signup(self):
        #self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        #self.browser.get('%s%s' % (self.live_server_url, '/login/'))
        '''
        f_name_input = self.selenium.find_element_by_name("f_name")
        f_name_input.send_keys('Monica')
        l_name_input = self.selenium.find_element_by_name("l_name")
        l_name_input.send_keys('Kuo')
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('mdk6jd')
        email1_input = self.selenium.find_element_by_name("email1")
        email1_input.send_keys('mdk6jd@virginia.edu')
        email2_input = self.selenium.find_element_by_name("email2")
        email2_input.send_keys('mdk6jd@virginia.edu')
        bio_input = self.selenium.find_element_by_name("bio")
        bio_input.send_keys('This is a test.')
        passowrd1_input = self.selenium.find_element_by_name("password1")
        password1_input.send_keys('something')
        password2_input = self.selenium.find_element_by_name("password2")
        password2_input.send_keys('something')
        self.selenium.find_element_by_name('Sign up!').click()
        '''

    '''
    def test_login(self):
        #self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.browser.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('mdk6jd')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('something')
    '''