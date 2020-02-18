from django.test import TestCase
import unittest
#from .models import Post
from models import Post

# Create your tests here.
class LemarsUnitTest(unittest.TestCase):

	# def test_blah(self):
	# 	title = "blah"

	# 	self.assertEqual(title, "blah")

	def test_update_post(self):
		# Arrange
		title = "My first run!"
		content = "Today I ran at Pismo Beach."
		distance = 5.4
		time = 36
		pace = round(distance/time, 2)
		date_posted = "2020-02-16"
		author = "Lemar"

		updated_content = "Actually it was at Morro Bay."

		self.post = Post(title = title, content = content, distance = distance, 
			time = time, date_posted = date_posted, author = author)

		# Act
		self.post.content = "Actually it was at Morro Bay."
		self.post.save()

		# Assert
		self.assertEqual(self.post.content, updated_content)



if __name__ == '__main__':
    unittest.main()