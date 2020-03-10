from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import *
import os
import random
import string

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



class TestSiteTitle(StaticLiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Chrome('UIATests/chromedriver')

	def tearDown(self):
		sleep(.1)
		self.driver.close()

	def test_title_is_Runn(self):
		self.driver.get(self.live_server_url)
		driver = self.driver
		self.assertIn("Runn", driver.title)

		runn_home_button = driver.find_element_by_xpath("/html/body/header/nav/a").text
		self.assertIn("Runn", runn_home_button)


class TestUserRegistration(StaticLiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Chrome('UIATests/chromedriver')

	def tearDown(self):
		sleep(.1)
		self.driver.close()

	def test_registration_success(self):
		# self.driver.get(self.live_server_url)
		self.driver.get("http://localhost:8000/")

		driver = self.driver
		driver.maximize_window()
		sleep(.3)
		register_button = driver.find_element_by_id("register_btn")
		register_button.click()

		username = randomString(12)
		email = username + '@gmail.com'
		name = username[:5]
		lastName = username[5:]

		registration_fields = {
			'//*[@id="id_username"]': username,
			'//*[@id="id_email"]': email,
			'//*[@id="id_first_name"]': name,
			'//*[@id="id_last_name"]': lastName,
			'//*[@id="id_bio"]': 'I am the zaniest boi',
			'//*[@id="id_location"]' : 'SLO',
			'//*[@id="id_password1"]' : 'runnpassword',
			'//*[@id="id_password2"]' : 'runnpassword'
		}

		for field in registration_fields:
			element = driver.find_element_by_xpath(field)
			element.send_keys(registration_fields[field])

		sign_up_button_xpath = '/html/body/main/div/div[1]/div/form/div/button'
		sign_up_button = driver.find_element_by_xpath(sign_up_button_xpath)
		sign_up_button.click()

		signup_feedback_box_xpath = '/html/body/main/div/div[1]/div'
		signup_feedback_box = driver.find_element_by_xpath(signup_feedback_box_xpath)
		self.assertTrue(username in driver.page_source)


class TestCreateNewPost(StaticLiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Chrome('UIATests/chromedriver')

	def tearDown(self):
		sleep(.1)
		self.driver.close()

	def test_create_new_post(self):
		self.driver.get("http://localhost:8000/")

		driver = self.driver
		driver.maximize_window()
		sleep(.3)
		register_button = driver.find_element_by_id("register_btn")
		register_button.click()


		# register
		username = randomString(12)
		email = username + '@gmail.com'
		name = username[:5]
		lastName = username[5:]

		registration_fields = {
			'//*[@id="id_username"]': username,
			'//*[@id="id_email"]': email,
			'//*[@id="id_first_name"]': name,
			'//*[@id="id_last_name"]': lastName,
			'//*[@id="id_bio"]': 'I am the zaniest boi',
			'//*[@id="id_location"]' : 'SLO',
			'//*[@id="id_password1"]' : 'runnpassword',
			'//*[@id="id_password2"]' : 'runnpassword'
		}

		for field in registration_fields:
			element = driver.find_element_by_xpath(field)
			element.send_keys(registration_fields[field])

		sign_up_button_xpath = '/html/body/main/div/div[1]/div/form/div/button'
		sign_up_button = driver.find_element_by_xpath(sign_up_button_xpath)
		sign_up_button.click()

		signup_feedback_box_xpath = '/html/body/main/div/div[1]/div'
		signup_feedback_box = driver.find_element_by_xpath(signup_feedback_box_xpath)
		self.assertTrue(username in driver.page_source)


		# create new post
		new_post_button = driver.find_element_by_xpath('//*[@id="navbarsExampleDefault"]/ul/div/li[3]/a')
		new_post_button.click()
		
		driver.find_element_by_xpath('//*[@id="id_distance"]').clear()
		driver.find_element_by_xpath('//*[@id="id_time"]').clear()

		title = 'test post title'
		content = 'test post content'
		distance = '4.0'
		time = "00:20:00"
		time_verif = '20'

		post_fields = {
			'//*[@id="id_title"]': title,
			'//*[@id="id_content"]': content,
			'//*[@id="id_distance"]': distance,
			'//*[@id="id_time"]': time
		}

		for field in post_fields:
			element = driver.find_element_by_xpath(field)
			element.send_keys(post_fields[field])
		

		post_button = driver.find_element_by_xpath('/html/body/main/div/div[1]/div/form/div/button')
		post_button.click()

		postText = driver.find_element_by_xpath('/html/body/main/div/div[1]/article[1]').text;

		title_element = driver.find_element_by_xpath('/html/body/main/div/div[1]/article[1]/div/h2/a/u')
		self.assertTrue(title in postText)
		self.assertTrue(content in postText)
		self.assertTrue(distance in postText)
		self.assertTrue(time_verif in postText)


class TestSearchForUser(StaticLiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Chrome('UIATests/chromedriver')

	def tearDown(self):
		sleep(.1)
		self.driver.close()

	def test_create_new_post(self):
		self.driver.get("http://localhost:8000/")

		driver = self.driver
		driver.maximize_window()
		sleep(.3)
		register_button = driver.find_element_by_id("register_btn")
		register_button.click()


		# register
		username = randomString(12)
		email = username + '@gmail.com'
		name = username[:5]
		lastName = username[5:]

		registration_fields = {
			'//*[@id="id_username"]': username,
			'//*[@id="id_email"]': email,
			'//*[@id="id_first_name"]': name,
			'//*[@id="id_last_name"]': lastName,
			'//*[@id="id_bio"]': 'I am the zaniest boi',
			'//*[@id="id_location"]' : 'SLO',
			'//*[@id="id_password1"]' : 'runnpassword',
			'//*[@id="id_password2"]' : 'runnpassword'
		}

		for field in registration_fields:
			element = driver.find_element_by_xpath(field)
			element.send_keys(registration_fields[field])

		sign_up_button_xpath = '/html/body/main/div/div[1]/div/form/div/button'
		sign_up_button = driver.find_element_by_xpath(sign_up_button_xpath)
		sign_up_button.click()

		signup_feedback_box_xpath = '/html/body/main/div/div[1]/div'
		signup_feedback_box = driver.find_element_by_xpath(signup_feedback_box_xpath)
		self.assertTrue(username in driver.page_source)


		# search for user named 'admin'
		search_button = driver.find_element_by_xpath("//*[@id=\"navbarsExampleDefault\"]/ul/li[2]/a")
		search_button.click()

		search_username = "admin"
		search_users_text_field = driver.find_element_by_xpath("/html/body/main/div/div/h2[2]/form/input")
		search_users_text_field.send_keys(search_username)

		search_by_name_button = driver.find_element_by_xpath("/html/body/main/div/div/h2[2]/form/button")
		search_by_name_button.click()

		admin_fname = 'adminfirstname'
		admin_lname = 'adminlastname'
		self.assertTrue(search_username in driver.page_source)
		self.assertTrue(admin_fname in driver.page_source)
		self.assertTrue(admin_lname in driver.page_source)


class TestSearchToProfileView(StaticLiveServerTestCase):
	def setUp(self):
		self.driver = webdriver.Chrome('UIATests/chromedriver')

	def tearDown(self):
		sleep(.1)
		self.driver.close()

	def test_create_new_post(self):
		self.driver.get("http://localhost:8000/")

		driver = self.driver
		driver.maximize_window()
		sleep(.3)
		register_button = driver.find_element_by_id("register_btn")
		register_button.click()


		# register
		username = randomString(12)
		email = username + '@gmail.com'
		name = username[:5]
		lastName = username[5:]

		registration_fields = {
			'//*[@id="id_username"]': username,
			'//*[@id="id_email"]': email,
			'//*[@id="id_first_name"]': name,
			'//*[@id="id_last_name"]': lastName,
			'//*[@id="id_bio"]': 'I am the zaniest boi',
			'//*[@id="id_location"]' : 'SLO',
			'//*[@id="id_password1"]' : 'runnpassword',
			'//*[@id="id_password2"]' : 'runnpassword'
		}

		for field in registration_fields:
			element = driver.find_element_by_xpath(field)
			element.send_keys(registration_fields[field])

		sign_up_button_xpath = '/html/body/main/div/div[1]/div/form/div/button'
		sign_up_button = driver.find_element_by_xpath(sign_up_button_xpath)
		sign_up_button.click()

		signup_feedback_box_xpath = '/html/body/main/div/div[1]/div'
		signup_feedback_box = driver.find_element_by_xpath(signup_feedback_box_xpath)
		self.assertTrue(username in driver.page_source)


		# search for user named 'admin'
		search_button = driver.find_element_by_xpath("//*[@id=\"navbarsExampleDefault\"]/ul/li[2]/a")
		search_button.click()

		search_username = "admin"
		search_users_text_field = driver.find_element_by_xpath("/html/body/main/div/div/h2[2]/form/input")
		search_users_text_field.send_keys(search_username)

		search_by_name_button = driver.find_element_by_xpath("/html/body/main/div/div/h2[2]/form/button")
		search_by_name_button.click()

		admin_fname = 'adminfirstname'
		admin_lname = 'adminlastname'
		self.assertTrue(search_username in driver.page_source)
		self.assertTrue(admin_fname in driver.page_source)
		self.assertTrue(admin_lname in driver.page_source)


		# click on user profile and verify info
		user_profile_page_link = driver.find_element_by_xpath("/html/body/main/div/div/li/a")
		user_profile_page_link.click()

		user_header_info = driver.find_element_by_xpath("/html/body/main/div/div[1]/div").text
		self.assertTrue(admin_fname in user_header_info)
		self.assertTrue(admin_lname in user_header_info)

		
		true_username = '@admin'
		self.assertTrue(true_username in user_header_info)


