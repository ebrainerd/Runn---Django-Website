from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User
import unittest

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

class RunPostTestCase(TestCase):

    def setUp(self):

        # Arrange and Act
        Run.objects.create(
            title="My best run!",
            content="I ran fast",
            distance=6.9,
            time=30,
            author=User.objects.create_user(username='Elliot',
                                            password='testing')
        )

    def testPostContents(self):

        # Assert
        my_post = Run.objects.get(title="My best run!")
        self.assertEqual(my_post.title, "My best run!")
        self.assertEqual(my_post.content, "I ran fast")
        self.assertEqual(my_post.distance, 6.9)
        self.assertEqual(my_post.time, 30)
        self.assertEqual(my_post.author, User.objects.get(username='Elliot'))

if __name__ == '__main__':
    unittest.main()
