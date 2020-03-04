from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse


class TestHomePage(StaticLiveServerTestCase):

	def setup(self):
		self.browser = webdriver.Chrome('UIATests/chromedriver')

	def teardown(self):
		self.browser.close()

	def test_stuff(self):
		self.browser.get(self.live_server_url)
		time.sleep(3)
