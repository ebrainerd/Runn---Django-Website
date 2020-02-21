import unittest
from models import Post
from django.contrib.auth.models import User


class TestPostCreation(unittest.TestCase):

	def test_post_fields(self):

			# Arrange
			title = 'Beach run'
			content = 'Today I ran on the beach with my dog bulgogi'
			distance = 4.2
			time = 30
			pace = round(distance/time, 2)
			author = User.objects.first()

			# Act
			new_post = Post(
				title=title,
				content=content,
				distance=distance,
				time=time,
				author=author)

			# Assert
			self.assertEqual(new_post.title, title)
			self.assertEqual(new_post.content, content)
			self.assertEqual(new_post.distance, distance)
			self.assertEqual(new_post.time, time)
			self.assertEqual(new_post.pace, pace)
			self.assertEqual(new_post.author, author)


