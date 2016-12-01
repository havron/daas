from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import os
import socket
import random

os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8000'

class SeleniumTests(StaticLiveServerTestCase):
   # fixtures = ['../../models/db.json']

    live_server_url = 'http://{}:8000'.format(
       socket.gethostbyname(socket.gethostname()))
    username = 'mdk6jd' + str(random.randrange(0, 9000))

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
        #self.browser.save_screenshot('register1.png')
        self.browser.get('%s%s' % (self.live_server_url, '/login/'))
        f_name_input = self.browser.find_element_by_name("f_name")
        f_name_input.send_keys('Monica')
        l_name_input = self.browser.find_element_by_name("l_name")
        l_name_input.send_keys('Kuo')
        username_input = self.browser.find_elements_by_name("username")[1]
        username_input.send_keys(self.username)
        self.browser.save_screenshot('username-entry.png')
        email1_input = self.browser.find_element_by_name("email1")
        email1_input.send_keys('mdk6jd@virginia.edu')
        email2_input = self.browser.find_element_by_name("email2")
        email2_input.send_keys('mdk6jd@virginia.edu')
        bio_input = self.browser.find_element_by_name("bio")
        bio_input.send_keys('This is a test.')
        password1_input = self.browser.find_element_by_name("password1")
        password1_input.send_keys('something')
        password2_input = self.browser.find_element_by_name("password2")
        password2_input.send_keys('something')
        #self.browser.save_screenshot('register3.png')
        self.browser.find_element_by_name('signup2').click()
        #print(self.browser.page_source)
        #print("TAKING SCREENSHOT")
        self.browser.save_screenshot('signedin.png')
        self.assertEquals(self.browser.current_url, self.live_server_url + "/register/")
        self.assertTrue("congrats, you registered" in self.browser.page_source)
        #print(self.browser.find_element_by_name("loginreponse"))

    
    def test_login(self):
        #self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        self.browser.get('%s%s' % (self.live_server_url, '/login/'))
        #self.browser.save_screenshot('register5.png')
        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys(self.username)
        password_input = self.browser.find_element_by_name("password")
        #self.browser.save_screenshot('register6.png')
        password_input.send_keys('something')
        self.browser.save_screenshot('login-entry.png')
        self.browser.find_element_by_name('loginbtn').click()
        self.browser.save_screenshot('loggedin.png')
        self.assertEquals(self.browser.current_url, self.live_server_url + "/")
        #self.browser.get((self.browser.current_url))
        #self.browser.find_element_by_name("Successfully logged in")


    
