from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import *
import os
import random
import string

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse




class TestSiteTitle(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('UIATests/chromedriver')

    # def tearDown(self):
    #     sleep(.1)
    #     self.driver.close()

    # def test_title_is_Runn(self):
    #     self.driver.get(self.live_server_url)
    #     driver = self.driver
    #     self.assertIn("Runn", driver.title)




    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.driver.find_element_by_xpath("//*[@id=\"id_username\"]")
        username_input.send_keys('admin')
        password_input = self.driver.find_element_by_xpath("//*[@id=\"id_password\"]")
        password_input.send_keys('runnpassword')
        self.driver.find_element_by_xpath('/html/body/main/div/div/div/form/div/button').click()



