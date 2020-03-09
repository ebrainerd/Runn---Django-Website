from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
import unittest
from unittest import skip


class LemarsUnitTest1(unittest.TestCase):

    def test_update_post(self):
        # Arrange
        title = "My first run!"
        content = "Today I ran at Pismo Beach."
        distance = 5.4
        time = "00:36:00"
        date_posted = "2020-02-16"

        updated_content = "Actually it was at Morro Bay."

        my_user = User.objects.create_user(username="lepopal", first_name="Lemar",
                                           last_name="Popal", email="lepopal@calpoly.edu")
        my_user.save()

        my_post = Post.objects.create(
            title=title,
            content=content,
            distance=distance,
            time=time,
            author=my_user.profile)

        my_post.save()

        # Act
        my_post.content = "Actually it was at Morro Bay."
        my_post.save()

        # Assert
        self.assertEqual(my_post.content, updated_content)


class LemarsUnitTest2(TestCase):

    def setUp(self):
        # Arrange and Act
        my_user = User.objects.create_user(username='johnlennon123', first_name='John',
                                           last_name='Lennon', email='lennon@thebeatles.com', password='johnpassword')
        my_user.save()

    def testUserContents(self):
        # Assert
        my_user = User.objects.get(username="johnlennon123")
        self.assertEqual(my_user.username, "johnlennon123")
        self.assertEqual(my_user.first_name, "John")
        self.assertEqual(my_user.last_name, "Lennon")
        self.assertEqual(my_user.email, "lennon@thebeatles.com")


class ElliotsUnitTest1(TestCase):

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
            time="00:30:00",
            author=my_user_profile)

    def testPostContents(self):
        # Assert
        my_post = Post.objects.get(title="My best run!")
        self.assertEqual(my_post.title, "My best run!")
        self.assertEqual(my_post.content, "I ran fast")
        self.assertEqual(my_post.distance, 6.9)
        self.assertEqual(my_post.time_minutes, 30)
        self.assertEqual(my_post.author, Profile.objects.get(user=User.objects.get(username='johnlennon123')))


if __name__ == '__main__':
    unittest.main()
