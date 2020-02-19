from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User

# Run tests from terminal with ./manage.py test

# To use test coverage:
#   pip install django-nose
#   ./manage.py test --with-coverage

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
