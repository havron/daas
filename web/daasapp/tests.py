from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class SeleniumTests(StaticLiveServerTestCase):
    fixtures = ['././models/db.json']

    @classmethod
    def setUpClass(cls):
        super(SeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_1signup(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
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

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('mdk6jd')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('something')