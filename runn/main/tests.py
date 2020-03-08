from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User
import unittest
from unittest import skip


@skip
class LemarsUnitTest(unittest.TestCase):

    def test_update_post(self):
        # Arrange
        title = "My first run!"
        content = "Today I ran at Pismo Beach."
        distance = 5.4
        time = 36
        pace = round(distance / time, 2)
        date_posted = "2020-02-16"

        updated_content = "Actually it was at Morro Bay."

        my_user = User.objects.create_user(username="lepopal", first_name="Lemar",
            last_name="Popal",email="lepopal@calpoly.edu")
        my_user.save()
        my_post = Post.objects.get_or_create(title=title, content=content, distance=distance,
                         time=time, date_posted=date_posted, author=my_user)


        # Act
        self.post.content = "Actually it was at Morro Bay."
        #self.post.save()

        # Assert
        self.assertEqual(self.post.content, updated_content)

@skip
class RunPostTestCase(TestCase):

    def setUp(self):
        # Arrange and Act
        my_user = User.objects.create_user(username='johnlennon123', first_name='John', 
            last_name='Lennon', email='lennon@thebeatles.com', password='johnpassword')
        my_user.save()

        my_user_profile = Profile.objects.get(user__username=my_user)

        Post.objects.create(
            title="My best run!",
            content="I ran fast",
            distance=6.9,
            time=30,
            author=my_user.username)

    def testPostContents(self):
        # Assert
        my_post = Post.objects.get(title="My best run!")
        self.assertEqual(my_post.title, "My best run!")
        self.assertEqual(my_post.content, "I ran fast")
        self.assertEqual(my_post.distance, 6.9)
        self.assertEqual(my_post.time, 30)
        self.assertEqual(my_post.author, User.objects.get(username='Elliot'))


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
